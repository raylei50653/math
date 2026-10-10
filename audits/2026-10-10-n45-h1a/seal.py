#!/usr/bin/env python3
"""Exclusive exact payload seal with observed read-only normal/seed17 and digest negative."""
import json
import os
import subprocess
import sys
from pathlib import Path
from checker import BASE,HERE,ROOT,META,sha,encoded,payload

def put(name,data):
    p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(data)

def main():
    table=payload()
    put('MANIFEST.sha256',''.join(v+'  '+k+'\n' for k,v in sorted(table.items())).encode())
    put('seal-checks/payload-before.json',encoded(table))
    commands=[]
    for label,seed,bad in [('normal',None,False),('seed17','17',False),('bad-digest',None,True)]:
        argv=[sys.executable,'-B',str(HERE/'checker.py'),'--check','--payload-only']
        env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'
        if seed:env['PYTHONHASHSEED']=seed
        if bad:
            raw=(HERE/'MANIFEST.sha256').read_bytes(); broken=b'0'*64+raw[64:]
            argv+=['--manifest','/dev/stdin']; supplied=broken
        else:supplied=None
        proc=subprocess.run(argv,input=supplied,cwd=ROOT,env=env,capture_output=True)
        stdout='seal-checks/'+label+'.stdout.txt';stderr='seal-checks/'+label+'.stderr.txt'
        put(stdout,proc.stdout);put(stderr,proc.stderr)
        expected=2 if bad else 0
        commands.append({'id':label,'command':argv,'cwd':str(ROOT),
                         'environment':{'PYTHONHASHSEED':seed} if seed else {},
                         'actual_exit':proc.returncode,'expected_exit':expected,
                         'stdout_file':stdout,'stdout_sha256':sha(proc.stdout),
                         'stderr_file':stderr,'stderr_sha256':sha(proc.stderr),
                         'stdin_sha256':sha(supplied) if supplied is not None else None})
        if proc.returncode!=expected:raise RuntimeError(label+': '+proc.stderr.decode())
    after=payload()
    assert after==table
    put('seal-checks/payload-after.json',encoded(after));put('seal-checks/commands.json',encoded(commands))
    bound={name:sha((HERE/name).read_bytes()) for name in sorted(META-{'MANIFEST.sha256','delivery.json','receipt.json'})}
    put('receipt.json',encoded({'task':'N45-H1A','scope':'exact observed seal metadata; not machine paper proof','files':bound}))
    bound['receipt.json']=sha((HERE/'receipt.json').read_bytes())
    put('delivery.json',encoded({'task':'N45-H1A','BASE':BASE,'decision':'accepted_HIGH1_with_full_H1_H13',
                                'manifest_file':'MANIFEST.sha256','manifest_sha256':sha((HERE/'MANIFEST.sha256').read_bytes()),
                                'payload_files':len(table),'receipt_bound_files':bound,
                                'REPORT_sha256':sha((HERE/'REPORT.md').read_bytes()),
                                'independent_judgment_sha256':sha((HERE/'independent-judgment.json').read_bytes()),
                                'evidence':'independent paper judgment; artifact checks only',
                                'new_Lean':False,'finite_source':'not performed; no HIGH1 trigger count','general_N2_E':'OPEN'}))
    proc=subprocess.run([sys.executable,'-B',str(HERE/'checker.py'),'--check'],cwd=ROOT,capture_output=True)
    if proc.returncode:raise RuntimeError(proc.stderr.decode())
    print(proc.stdout.decode().strip())
    print(json.dumps({'manifest_sha256':sha((HERE/'MANIFEST.sha256').read_bytes()),'payload_files':len(table),
                      'receipt_bound_metadata':len(bound),'full_readonly_check_exit':proc.returncode},sort_keys=True))

if __name__=='__main__':main()
