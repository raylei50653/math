#!/usr/bin/env python3
"""Run artifact/documentation checks, logging commands; never alter shared files."""
from pathlib import Path
import hashlib, io, json, subprocess, tarfile
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
records=[]
def write(path, data):
    target=OUT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f:
        f.write(data if isinstance(data,bytes) else data.encode())
def run(name,argv,cwd=ROOT,expect=0,env=None):
    p=subprocess.run(argv,cwd=cwd,capture_output=True,env=env)
    write(f'logs/{name}.stdout.log',p.stdout)
    write(f'logs/{name}.stderr.log',p.stderr)
    records.append({'id':name,'argv':argv,'cwd':str(cwd),'exit_code':p.returncode,
                    'expected_exit':expect,'exit_matches_expectation':p.returncode==expect,
                    'stdout':f'logs/{name}.stdout.log','stderr':f'logs/{name}.stderr.log'})
    return p
archive=run('base-archive',['git','archive','--format=tar',BASE])
if archive.returncode:
    raise SystemExit('BASE archive failed')
source=OUT/'base-source'
source.mkdir(exist_ok=False)
with tarfile.open(fileobj=io.BytesIO(archive.stdout),mode='r:') as tf:
    tf.extractall(source,filter='data')
write('base-archive.json',json.dumps({'base':BASE,'sha256':hashlib.sha256(archive.stdout).hexdigest(),
                                    'source':'base-source','scope':'exact Git archive; no worktree registrations'},indent=2)+'\n')
run('base-docs',['python3','-B','scripts/check_docs.py'],source,expect=1)
run('base-formal-docgraph',['python3','-B','tools/docgraph','--include','docs/**/*.md','check'],source)
run('current-docs',['python3','-B','scripts/check_docs.py'])
run('current-formal-docgraph',['python3','-B','tools/docgraph','--include','docs/**/*.md','check'])
run('current-whole-docgraph',['python3','-B','tools/docgraph','check'],expect=1)
run('tracked-diff-check',['git','diff','--check'])
run('cached-diff-check',['git','diff','--cached','--check'])
run('final-head',['git','rev-parse','HEAD'])
run('final-status',['git','status','--short','--branch'])
run('final-shared-diff',['git','diff','--binary'])
run('final-shared-cached-diff',['git','diff','--cached','--binary'])
write('documentation-checks.json',json.dumps(records,indent=2)+'\n')
print(json.dumps([{'id':r['id'],'exit_code':r['exit_code'],'expected_exit':r['expected_exit']} for r in records],indent=2))
