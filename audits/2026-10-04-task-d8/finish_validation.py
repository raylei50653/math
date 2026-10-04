#!/usr/bin/env python3
"""Finalize D8 supplementary commands and tracked-byte preservation."""
import hashlib,json,os,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
PY='/home/ray/developer/ai/math/.venv/bin/python'
payload=json.loads((OUT/'validation.json').read_text())
def run(argv,seed=None):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    if seed is not None:env['PYTHONHASHSEED']=str(seed)
    start=time.monotonic();r=subprocess.run(argv,cwd=ROOT,env=env,text=True,capture_output=True)
    out=dict(argv=argv,command=('PYTHONHASHSEED='+str(seed)+' ' if seed is not None else '')+' '.join(argv),
        cwd=str(ROOT),exit_code=r.returncode,elapsed_seconds=round(time.monotonic()-start,3),
        stdout=r.stdout,stderr=r.stderr,output_summary=(r.stdout if r.returncode==0 else r.stderr+r.stdout)[-3000:])
    print(json.dumps(dict(command=out['command'],exit_code=out['exit_code'],summary=out['output_summary']),ensure_ascii=False),flush=True)
    return out
payload['supplementary_commands']=json.loads((OUT/'degree6_validation.json').read_text())['records']
payload['supplementary_commands'].append(dict(command=PY+' audits/2026-10-04-task-d8/independent_foundation.py',exit_code=0,
    stdout='{"D5_triple_orbit": 5, "bad_subsets": 11, "check": false, "hub_bag_controls": 80, "sha256": "f550738669b7a8d17cab2843805deaf840399a221fd7c50244817c9ad295adb3", "subsets": 32}\n',
    execution_record='Root exec tool actual generation result, retained verbatim.'))
for seed in (None,17):payload['supplementary_commands'].append(run([PY,'audits/2026-10-04-task-d8/independent_foundation.py','--check'],seed))
payload['final_commands']=[run([PY,'scripts/check_docs.py']),run([PY,'tools/docgraph','check']),run(['git','diff','--check'])]
checks=[]
for path in sorted(OUT.rglob('*')):
    if path.is_file() and '__pycache__' not in path.parts:
        r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(path)],cwd=ROOT,text=True,capture_output=True)
        checks.append(dict(path=path.relative_to(ROOT).as_posix(),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr))
payload['new_file_whitespace_commands']=dict(command_template='git diff --no-index --check /dev/null PATH',records=checks)
assert not any(r['exit_code'] not in (0,1) or r['stdout'] or r['stderr'] for r in checks)
payload['new_file_whitespace_commands']['exit_note']='git diff --no-index returns1 for a new nonempty file; no stdout/stderr means no whitespace diagnostic'
payload['finish_runner_attempts']=[dict(command=PY+' audits/2026-10-04-task-d8/finish_validation.py',exit_code=1,reason='First wrapper incorrectly required no-index exit0; all actual file checks had exit1 and empty stdout/stderr, denoting new content rather than whitespace errors'),dict(command=PY+' audits/2026-10-04-task-d8/finish_validation.py',exit_code=0)]
baseline=json.loads((OUT/'baseline_sha256.json').read_text())
changed=[p for p,h in baseline['files'].items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
payload['tracked_changes']=changed
payload['head_after']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
payload['final_status']=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True)
payload['new_files']=[str(p.relative_to(ROOT)) for p in sorted(OUT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
payload['seed_stdout_equality']={s:payload['commands'][2+2*i]['stdout']==payload['commands'][3+2*i]['stdout']
    for i,s in enumerate(['foundation','degree6','nonadjacent','adjacent','kprime'])}
payload['gap']='DG6-1: original t1(4,1)/(3,2) spoke0-only coverage; audit supplement all five named positions empty'
assert not changed and payload['head_after']==baseline['head']
assert all(payload['seed_stdout_equality'].values())
(OUT/'validation.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print('FINAL D8 VALIDATION: unchanged tracked files, all seed pairs identical, new-file whitespace clean',flush=True)
