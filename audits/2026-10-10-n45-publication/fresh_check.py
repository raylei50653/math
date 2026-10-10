#!/usr/bin/env python3
"""Export the candidate index to an isolated real Git checkout and restore bytes."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def main():
    spec=importlib.util.spec_from_file_location('runs',HERE/'run_checks.py')
    runs=importlib.util.module_from_spec(spec);spec.loader.exec_module(runs)
    candidate=Path(tempfile.mkdtemp(prefix='n45-publication-candidate-'))
    records=[]
    records.append(runs.run('fresh-clone',['git','clone','--shared','--no-checkout','--quiet',str(ROOT),str(candidate)]))
    assert records[-1]['exit_code']==0
    records.append(runs.run('fresh-export-index',['git','checkout-index','--all','--prefix='+str(candidate)+'/']))
    assert records[-1]['exit_code']==0
    with (HERE/'fresh-candidate.json').open('x') as f:json.dump({'path':str(candidate),'method':'actual Git clone --shared --no-checkout at research BASE, then exact current candidate Git index export; no HEAD impersonation'},f,indent=2);f.write('\n')
    for name,argv in [
        ('fresh-legacy-restore',['python3','-B','tools/audit_archive.py','restore','--artifacts']),
        ('fresh-n45-restore',['python3','-B','audits/2026-10-10-n45-publication/archive.py','restore']),
    ]:
        records.append(runs.run(name,argv,cwd=candidate))
        assert records[-1]['exit_code']==0,records[-1]
    jobs=[
        ('fresh-publication-normal',['python3','-B','audits/2026-10-10-n45-publication/verify.py'],None),
        ('fresh-publication-seed17',['python3','-B','audits/2026-10-10-n45-publication/verify.py'],17),
        ('fresh-docs',['python3','-B','scripts/check_docs.py'],None),
        ('fresh-docgraph-docs',['python3','-B','tools/docgraph','--include','docs/**/*.md','check'],None),
    ]
    with ThreadPoolExecutor(max_workers=4) as pool:
        records+=list(pool.map(lambda j:runs.run(j[0],j[1],cwd=candidate,seed=j[2]),jobs))
    records.append(runs.run('staged-whitespace',['git','diff','--cached','--check']))
    normal=next(r for r in records if r['name']=='fresh-publication-normal')
    seed=next(r for r in records if r['name']=='fresh-publication-seed17')
    summary={'candidate':str(candidate),'executions':records,
             'normal_seed17_stdout_identical':normal['stdout_sha256']==seed['stdout_sha256'],
             'original_worktree_inputs_modified':False,'new_Lean':False,
             'candidate_HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=candidate).decode().strip()}
    with (HERE/'fresh-validation.json').open('x') as f:json.dump(summary,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({'exits':{r['name']:r['exit_code'] for r in records},'normal_seed17_identical':summary['normal_seed17_stdout_identical']},sort_keys=True))
    assert all(r['exit_code']==0 for r in records)
    assert summary['normal_seed17_stdout_identical']


if __name__=='__main__':main()
