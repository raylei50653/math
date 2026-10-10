#!/usr/bin/env python3
"""Create this fresh audit seal once; never edits frozen input or shared files."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOGS = {f'receipt/{name}.{stream}.log' for name in ('normal','seed17') for stream in ('stdout','stderr')}
EXCLUDED = {'MANIFEST.sha256','delivery.json','receipt.json'}|LOGS

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name,value):
    with (HERE/name).open('x') as f:
        json.dump(value,f,sort_keys=True,indent=2)
        f.write('\n')

require_absent = [HERE/name for name in ('MANIFEST.sha256','delivery.json','receipt.json')]
assert not any(p.exists() for p in require_absent), 'Already sealed or failed staging: preserve bytes and stop'
files = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and p.relative_to(HERE).as_posix() not in EXCLUDED)
with (HERE/'MANIFEST.sha256').open('x') as f:
    for relative in files:
        f.write(sha(HERE/relative)+'  '+relative+'\n')
(HERE/'receipt').mkdir()
commands = []
for name in ('normal','seed17'):
    env = os.environ.copy()
    if name=='seed17':
        env['PYTHONHASHSEED']='17'
    else:
        env.pop('PYTHONHASHSEED',None)
    command = [sys.executable,'-B',str(HERE/'verify.py'),'--payload-only']
    before = sha(HERE/'MANIFEST.sha256')
    run = subprocess.run(command,cwd=ROOT,env=env,capture_output=True)
    (HERE/f'receipt/{name}.stdout.log').write_bytes(run.stdout)
    (HERE/f'receipt/{name}.stderr.log').write_bytes(run.stderr)
    commands.append({'name':name,'command':command,'cwd':str(ROOT),'PYTHONHASHSEED':env.get('PYTHONHASHSEED'),
                     'exit_code':run.returncode,'stdout':f'receipt/{name}.stdout.log','stderr':f'receipt/{name}.stderr.log',
                     'payload_before':before,'payload_after':sha(HERE/'MANIFEST.sha256'),
                     'boundary':'Actual read-only payload/incoming-receipt verification; this audit outer receipt is not yet constructed'})
    if run.returncode:
        write('failed-seal.json',{'failed':name,'commands':commands,'stdout':run.stdout.decode(),'stderr':run.stderr.decode()})
        print(run.stderr.decode(),file=sys.stderr)
        sys.exit(run.returncode)
assert (HERE/'receipt/normal.stdout.log').read_bytes()==(HERE/'receipt/seed17.stdout.log').read_bytes()
write('receipt.json',{'commands':commands,'metadata':{p:sha(HERE/p) for p in sorted(LOGS)},
                      'scope':'Only this audit metadata logs are excluded and bound here; all nested manifests/deliveries/receipts are payload'})
write('delivery.json',{'task':'N45-L2R','BASE':'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744',
                       'manifest_sha256':sha(HERE/'MANIFEST.sha256'),'receipt_sha256':sha(HERE/'receipt.json'),
                       'payload_count':len(files),'excluded_exact_paths':sorted(EXCLUDED),
                       'paper_verdict':'All six LOW2 claims accepted under the complete stated contract; independent paper review, not machine proof',
                       'source_controls':'not established; not executed; no trigger count','new_Lean':False,
                       'shared_edits_commit_push_PR_external_messages':False})
print(json.dumps({'payload_files':len(files),'manifest_sha256':sha(HERE/'MANIFEST.sha256'),'receipt_sha256':sha(HERE/'receipt.json'),
                  'normal_exit':commands[0]['exit_code'],'seed17_exit':commands[1]['exit_code'],'stdout_byte_equal':True},sort_keys=True))
