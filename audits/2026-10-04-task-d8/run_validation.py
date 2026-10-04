#!/usr/bin/env python3
"""D8 replay runner; preserves every tracked baseline byte."""
import concurrent.futures, hashlib, json, os, shutil, subprocess, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PY='/home/ray/developer/ai/math/.venv/bin/python'
ENV=dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
records=[]
def run(argv, seed=None):
    env=dict(ENV)
    if seed is not None: env['PYTHONHASHSEED']=str(seed)
    start=time.monotonic()
    p=subprocess.run(argv,cwd=ROOT,env=env,text=True,capture_output=True)
    return dict(argv=argv, command=('PYTHONHASHSEED='+str(seed)+' ' if seed is not None else '')+' '.join(argv),
        cwd=str(ROOT),exit_code=p.returncode,elapsed_seconds=round(time.monotonic()-start,3),
        stdout=p.stdout,stderr=p.stderr,output_summary=p.stdout[:1600] if p.returncode==0 else (p.stderr+p.stdout)[-2500:])
def add(r):
    records.append(r); print(json.dumps(dict(command=r['command'],exit_code=r['exit_code'],summary=r['output_summary']),ensure_ascii=False),flush=True)
def hashes():
    files=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    return {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files if f and (ROOT/f).is_file()}
before=hashes()
head_before=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
with (OUT/'baseline_sha256.json').open('x') as f:json.dump(dict(head=head_before,files=before),f,indent=2)
manifest=json.loads((ROOT/'artifacts/MANIFEST.json').read_text())
restored=[]
# Only missing ignored runtime files are rebuilt, as explicitly authorized.
if not (ROOT/'artifacts/c5_excess_two_e3/degree6.json').exists():
    add(run([PY,'scripts/c5_excess_two_e3_degree6.py']))
    restored.append('artifacts/c5_excess_two_e3/degree6.json')
kp=['artifacts/c5_kempe_diagonal_transport/assignments.jsonl','artifacts/c5_kempe_diagonal_transport/bounded_realization.json']
if any(not (ROOT/p).exists() for p in kp):
    fresh=OUT/'rebuilt_kprime'
    result=run([PY,'scripts/c5_kempe_diagonal_transport.py','--output',str(fresh)])
    add(result)
    if result['exit_code']==0:
        for source in sorted(fresh.iterdir()):
            target=ROOT/'artifacts/c5_kempe_diagonal_transport'/source.name
            payload=source.read_bytes()
            if target.exists():
                assert target.read_bytes()==payload, 'Regeneration differs from tracked baseline '+str(target)
            else:
                rel=target.relative_to(ROOT).as_posix(); expected=manifest['files'][rel]
                assert len(payload)==expected['bytes'] and hashlib.sha256(payload).hexdigest()==expected['sha256']
                with target.open('xb') as f:f.write(payload)
                restored.append(rel)
            if target.name not in {Path(p).name for p in kp}: source.unlink()
checks=['scripts/c5_excess_two_e3_foundation.py','scripts/c5_excess_two_e3_degree6.py','scripts/c5_excess_two_e3_nonadjacent.py','scripts/c5_excess_two_e3_adjacent.py','scripts/c5_kempe_diagonal_transport.py']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    jobs=[pool.submit(run,[PY,s,'--check'],seed) for s in checks for seed in (None,17)]
    for j in jobs:add(j.result())
for argv in ([PY,'scripts/check_docs.py'],[PY,'tools/docgraph','check'],['git','diff','--check']):add(run(argv))
after=hashes()
changed=[f for f in before if before[f]!=after.get(f)]
head_after=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
status=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True)
result=dict(schema=1,baseline=head_before,head_after=head_after,python=PY,
    environment={'PYTHONDONTWRITEBYTECODE':'1'},commands=records,
    missing_runtime_files_rebuilt=restored,tracked_file_count=len(before),tracked_changes=changed,
    final_status=status,archive_scope='D2 integration diff and D5 scope_ledger not restored; known missing paths are recorded by check_docs',
    evidence_boundary='Checker byte replay and controls do not prove arbitrary-size paper arguments or topology.')
with (OUT/'validation.json').open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
assert not changed and head_before==head_after
print('VALIDATION WRITTEN; tracked changes',len(changed),flush=True)
