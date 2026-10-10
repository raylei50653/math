#!/usr/bin/env python3
"""Exclusive seal, followed by strict read-only input/delivery replay."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
records=[]
def write(rel,data):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(data if isinstance(data,bytes) else data.encode())
def run(name,args,prefix='logs',seed=None):
    env=os.environ.copy()
    if seed is not None:env['PYTHONHASHSEED']=seed
    p=subprocess.run(args,cwd=ROOT,env=env,capture_output=True)
    write(f'{prefix}/{name}.stdout.log',p.stdout);write(f'{prefix}/{name}.stderr.log',p.stderr)
    rec={'id':name,'argv':args,'cwd':str(ROOT),'exit_code':p.returncode,
         'stdout':f'{prefix}/{name}.stdout.log','stderr':f'{prefix}/{name}.stderr.log','env':{'PYTHONHASHSEED':seed} if seed is not None else {}}
    records.append(rec)
    if p.returncode:raise RuntimeError(f'{name} exit {p.returncode}: '+p.stderr.decode())
    return p
normal=run('verify-preseal-normal',['python3','-B',str(OUT/'verify.py'),'--preseal'])
seed=run('verify-preseal-seed17',['python3','-B',str(OUT/'verify.py'),'--preseal'],seed='17')
assert normal.stdout==seed.stdout,'preseal results differ'
commands=[]
for name in ['bootstrap-checks.json','supplement-checks.json','documentation-checks.json']:
    commands+=json.loads((OUT/name).read_text())
commands+=[json.loads((OUT/'gallai-extract-check.json').read_text()),json.loads((OUT/'verify-initial-check.json').read_text())]
commands+=records
checks={'task':'N45-U-SS','base':BASE,'scope':'Input/artifact/documentation verification; no finite source calculation or new Lean',
        'commands':commands,'preseal_normal_seed17_byte_equal':True,
        'postseal_commands':'seal-checks/commands.json',
        'historical_failures':{'E4_byte_replays':'Retained prior FAIL; not rerun','BASE_check_docs':'Freshly reproduced two missing paths; exit1','whole_worktree_DocGraph':'Freshly reproduced 62 duplicate-ID errors; exit1'},
        'not_run':['All upstream mathematical/source checkers','PC/PCA LP checker as SS control','New graph/k search','Lean build/axioms','Remote CI'],
        'write_scope':'Only this fresh audit; all pre-existing shared tracked/untracked file hashes and inventory checked unchanged.'}
write('checks.json',json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
# MANIFEST covers exact payload, excluding seal metadata only.
excluded={'MANIFEST.sha256','delivery.json'}
files=sorted(p for p in OUT.rglob('*') if p.is_file() and str(p.relative_to(OUT)) not in excluded and not str(p.relative_to(OUT)).startswith('seal-checks/'))
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(OUT))+'\n' for p in files)
write('MANIFEST.sha256',manifest)
write('delivery.json',json.dumps({'task':'N45-U-SS','base':BASE,'head':BASE,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'output':str(OUT.relative_to(ROOT)),'report':'REPORT.md','claims':'claims.json','mathematical_status':'Arbitrary-size SS paper candidate under the entire stated contract; independent incremental audit and adoption pending.',
 'manifest':'MANIFEST.sha256','manifest_sha256':hashlib.sha256(manifest.encode()).hexdigest(),'payload_file_count':len(files),
 'excluded_from_payload_manifest':['MANIFEST.sha256','delivery.json','seal-checks/**'],
 'exclusion_reason':'Manifest and delivery metadata do not self-hash; postseal read-only replay logs have a separate metadata manifest.',
 'postseal_checks':'seal-checks/commands.json','postseal_manifest':'seal-checks/MANIFEST.sha256',
 'shared_changes':False,'commit_push_pr_external_messages_subagents':False,'new_Lean':False,'new_source_realization':False,'new_finite_source_certificate':False,
 'stopping_point':'Return for independent incremental adjudication; no next residual selected.'},indent=2,ensure_ascii=False)+'\n')
args=['python3','-B',str(OUT/'verify.py')]
start=len(records)
(OUT/'seal-checks').mkdir(exist_ok=False)
# Create the command-log target exclusively, then write its actual results once both runs finish.
with (OUT/'seal-checks/commands.json').open('x') as command_log:
    sealed_normal=run('verify-sealed-normal',args,prefix='seal-checks')
    sealed_seed=run('verify-sealed-seed17',args,prefix='seal-checks',seed='17')
    assert sealed_normal.stdout==sealed_seed.stdout,'sealed results differ'
    command_log.write(json.dumps({'task':'N45-U-SS','normal_seed17_byte_equal':True,'commands':records[start:]},indent=2)+'\n')
metadata=sorted(p for p in (OUT/'seal-checks').iterdir() if p.is_file() and p.name!='MANIFEST.sha256')
write('seal-checks/MANIFEST.sha256',''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in metadata))
print(json.dumps({'task':'N45-U-SS','payload_files':len(files),'main_manifest_sha256':hashlib.sha256(manifest.encode()).hexdigest(),
                 'preseal_normal_seed17_equal':True,'sealed_normal_seed17_equal':True,
                 'sealed_verification':json.loads(sealed_normal.stdout)},indent=2))
