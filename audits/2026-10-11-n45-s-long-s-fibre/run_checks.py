#!/usr/bin/env python3
"""Execute retained read-only checks, preserving failures and negative input."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request
from setup import BASE, OUT, ROOT, dump, run, write

if __name__=='__main__':
    initial=(OUT/'inputs.json').read_bytes()
    write(OUT/'inputs-initial.json',initial)
    data=json.loads(initial)
    path='docs/c5_degree4_guide.md'
    p=run('supplement-degree4-guide',['git','show',f'{BASE}:{path}'])
    assert p.returncode==0 and p.stdout==(ROOT/path).read_bytes()
    blob=run('supplement-degree4-blob',['git','rev-parse',f'{BASE}:{path}']).stdout.decode().strip()
    write(OUT/'frozen'/path,p.stdout)
    data['entries'].append({'path':path,'base':BASE,'git_blob':blob,'sha256':hashlib.sha256(p.stdout).hexdigest(),
       'bytes':len(p.stdout),'frozen_path':'frozen/'+path,'worktree_matches_base':True,'kind':'BASE Git blob'})
    # External primary theorem: bytes frozen separately, no Git authority claimed.
    url=data['external_dependencies'][0]['url']
    try:
        raw=urllib.request.urlopen(url,timeout=30).read()
        write(OUT/'external/gallai.pdf',raw)
        data['external_dependencies'][0].update({'frozen_path':'external/gallai.pdf',
          'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
        dump(OUT/'logs/external-fetch.json',{'url':url,'method':'urllib.request.urlopen','timeout_seconds':30,
           'exit':0,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    except Exception as exc:
        dump(OUT/'logs/external-fetch.json',{'url':url,'exit':1,'error':repr(exc)})
    (OUT/'inputs.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    for n,pth in enumerate(('docs/c5_short_component_local.md','docs/c5_shared_two_cycles.md')):
        p=run(f'exploratory-missing-{n}',['git','show',f'{BASE}:{pth}'])
        assert p.returncode!=0
    dump(OUT/'logs/exploratory-keyerror.json',{'kind':'retained actual exploratory failure',
        'command':"python3: inspect controls using d['roots']",'exit':1,'stdout':'',
        'stderr':"Traceback (most recent call last):\n  File \"<stdin>\", line 4, in <module>\nKeyError: 'roots'\n",
        'repair':'Infer roots from original piece owners. No generation or input was overwritten.'})
    checker='audits/2026-10-11-n45-s-long-s-fibre/checker.py'
    checks=[]
    for name,env in [('replay',None),('replay-seed17',dict(os.environ,PYTHONHASHSEED='17'))]:
        r=run(name,['python3','-B',checker,'--check'],env)
        checks.append({'name':name,'exit':r.returncode,'status':'triggered and holds' if r.returncode==0 else 'counterexample'})
    bad=json.loads((OUT/'certificate.json').read_text())
    bad['controls'][0]['rows'][0]['C']['assignments'][0][0]=99
    dump(OUT/'negative-corrupt-certificate.json',bad)
    r=run('negative-corrupt-certificate',['python3','-B',checker,'--check','--certificate',str(OUT/'negative-corrupt-certificate.json')])
    assert r.returncode!=0
    checks.append({'name':'corrupt complete C assignment rejected','exit':r.returncode,'expected_failure':True,'status':'triggered and holds'})
    r=run('negative-exclusive-create',['python3','-B',checker,'--write'])
    assert r.returncode!=0
    checks.append({'name':'existing canonical certificate preserved','exit':r.returncode,'expected_failure':True,'status':'triggered and holds'})
    r=run('diff-check',['git','diff','--check'])
    checks.append({'name':'git diff --check','exit':r.returncode,'status':'triggered and holds' if not r.returncode else 'counterexample'})
    cert=json.loads((OUT/'certificate.json').read_text())
    dump(OUT/'checks.json',{'checks':checks,'counts':cert['counts'],
       'finite_source':cert['finite_source'],
       'BASE_final_JSON_replay':{'status':'not triggered','reason':'No blob at supplied BASE; source finding retained.'},
       'Lean':{'executed':False,'new_theorem':False},
       'external_fetch':'logs/external-fetch.json'})
    print(json.dumps({'checks':checks,'counts':cert['counts']},ensure_ascii=False))
