#!/usr/bin/env python3
"""Run the necessary publication checks and preserve actual inventory rejection."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def main():
    spec=importlib.util.spec_from_file_location('runs',HERE/'run_checks.py')
    runs=importlib.util.module_from_spec(spec);spec.loader.exec_module(runs)
    jobs=[
        ('publication-normal',['python3','-B',str(HERE/'verify.py')],None,0),
        ('publication-seed17',['python3','-B',str(HERE/'verify.py')],17,0),
        ('archive-verify',['python3','-B',str(HERE/'archive.py'),'verify'],None,0),
        ('docs',['python3','-B','scripts/check_docs.py'],None,0),
        ('docgraph-docs',['python3','-B','tools/docgraph','--include','docs/**/*.md','check'],None,0),
        ('docgraph-whole',['python3','-B','tools/docgraph','check'],None,1),
        ('diff-check',['git','diff','--check'],None,0),
    ]
    with ThreadPoolExecutor(max_workers=7) as pool:
        results=list(pool.map(lambda j:runs.run(j[0],j[1],seed=j[2],expected=j[3]),jobs))
    negative=json.loads((HERE/'inputs.json').read_text())
    omitted='audits/2026-10-10-n45-high23-supervision/frozen/audits/2026-10-10-n45-s-high2/receipt.json'
    del negative['files'][omitted]
    data=(json.dumps(negative,ensure_ascii=False,indent=2)+'\n').encode()
    with (HERE/'negative-inputs.json').open('xb') as f:f.write(data)
    results.append(runs.run('negative-nested-omission',['python3','-B',str(HERE/'verify.py'),'--inputs-stdin'],expected=2,stdin=data))
    summary={'executions':results,'normal_seed17_stdout_identical':results[0]['stdout_sha256']==results[1]['stdout_sha256'],'negative_omitted':omitted,'historical_FAIL_preserved':True,'new_Lean':False,'finite_source':'not established/not executed'}
    with (HERE/'prestage-validation.json').open('x') as f:json.dump(summary,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({'exits':{r['name']:r['exit_code'] for r in results},'normal_seed17_identical':summary['normal_seed17_stdout_identical']},sort_keys=True))
    assert all(r['exit_code']==r['expected_exit'] for r in results)
    assert summary['normal_seed17_stdout_identical']


if __name__=='__main__':main()
