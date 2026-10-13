#!/usr/bin/env python3
"""Check docs and storage without changing the real index or old artifacts.
Use --audit-links after DELIVERY.json exists. Normal run writes its own receipts.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]

def audit_links():
    spec=importlib.util.spec_from_file_location('docs_checker',REPO/'scripts/check_docs.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    errors=[];count=0;files=sorted(ROOT.rglob('*.md'))
    for source in files:
        for line,destination in mod.links(source.read_text()):
            url=urlsplit(destination)
            if url.scheme or url.netloc:continue
            count+=1;target=(source.parent/unquote(url.path)).resolve() if url.path else source
            if not target.exists():errors.append(f'{source.relative_to(ROOT)}:{line}: missing {destination}')
            elif url.fragment and target.suffix=='.md' and unquote(url.fragment) not in mod.anchors(target.read_text()):
                errors.append(f'{source.relative_to(ROOT)}:{line}: missing anchor {destination}')
    assert not errors,errors
    return {'status':'PASS','files':len(files),'links':count}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--audit-links',action='store_true');args=ap.parse_args()
    if args.audit_links:print(json.dumps(audit_links(),sort_keys=True));return
    records=[]
    def run(name,args,expected=0,env=None):
        result=subprocess.run(args,cwd=REPO,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log=ROOT/'logs'/f'{name}.log'
        with log.open('xb') as f:f.write(result.stdout)
        receipt={'name':name,'command':args,'returncode':result.returncode,'expected':expected,'log':str(log.relative_to(ROOT))}
        records.append(receipt);assert result.returncode==expected,receipt
    run('final-check-docs',['python3','-B','scripts/check_docs.py'])
    run('final-docgraph-formal',['python3','-B','tools/docgraph','--include','docs/**/*.md','check'])
    run('final-docgraph-global',['python3','-B','tools/docgraph','check'],expected=1)
    baseline=(ROOT/'logs/base-docgraph-global.log').read_bytes();final=(ROOT/'logs/final-docgraph-global.log').read_bytes()
    assert baseline==final,'global DocGraph error set drift'
    assert final.count(b'ERROR [duplicate-id]')==62
    run('final-whitespace',['git','diff','--check'])
    # Include each new deliverable in a temporary index/object database only.
    index=REPO/'.git/index';before=hashlib.sha256(index.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='w5-rank4-storage-') as td:
        td=Path(td);(td/'objects').mkdir()
        env=os.environ.copy();env.update(GIT_INDEX_FILE=str(td/'index'),GIT_OBJECT_DIRECTORY=str(td/'objects'),GIT_ALTERNATE_OBJECT_DIRECTORIES=str(REPO/'.git/objects'))
        subprocess.run(['git','read-tree','HEAD'],cwd=REPO,env=env,check=True)
        files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
        paths=[str(p.relative_to(REPO)) for p in files]
        subprocess.run(['git','-c','core.fsmonitor=false','add','-f','--',*paths],cwd=REPO,env=env,check=True)
        run('storage-temporary-index',['python3','-B','tools/check_generated_artifacts.py'],env=env)
        policy={'files':len(files),'paths':paths,'real_index_unchanged':True,'objects_written_only_to_tmp':True}
    assert hashlib.sha256(index.read_bytes()).hexdigest()==before
    assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=REPO)
    # All new JSON-like outputs obey the same 1 MB size threshold, including
    # receipts created after the temporary-index snapshot.
    large=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl','.ndjson','.json5','.bin') and p.stat().st_size>=1000000]
    assert not large,large
    existing={
      'base_check_docs':{'returncode':0,'log':'logs/base-check-docs.log'},
      'base_global_docgraph':{'returncode':1,'errors':62,'log':'logs/base-docgraph-global.log'},
      'lake_build':{'returncode':0,'command':['lake','build'],'log':'logs/lake-build.log','new_Lean_theorem':False},
      'storage_tools_tests':{'returncode':0,'command':['.venv/bin/python','-B','-m','unittest','discover','-s','tools/tests','-p','test_*.py'],'log':'logs/storage-tests-venv.log','prior_missing_networkx_failure':'logs/storage-tests.log'},
      'primary':{'receipt':'controls/results.json'},
      'independent_normal':{'returncode':0,'command':['python3','-B',str(ROOT.relative_to(REPO)/'independent/check.py')],'log':'logs/independent-replay.log'},
      'independent_seed17':{'returncode':0,'environment':{'PYTHONHASHSEED':'17'},'command':['python3','-B',str(ROOT.relative_to(REPO)/'independent/check.py')],'log':'logs/independent-replay-seed17.log'},
      'negative_generation_v2':{'returncode':0,'log':'logs/negative-generate-v2.log','prior_harness_failure_retained':'logs/negative-generate.log'},
      'negative_replay_seed17':{'returncode':0,'log':'logs/negative-replay-seed17.log'},
      'independent_domain_and_geometry':{'returncode':0,'receipt':'review/domain-review.json'},
      'certificate_metadata':{'returncode':0,'receipt':'logs/certificate-metadata.json'},
    }
    for name in ('independent_normal','independent_seed17'):
        obj=json.loads((ROOT/existing[name]['log']).read_text().splitlines()[-1]);assert obj['templates']==6389 and obj['status']=='PASS independent exact comparison'
    assert 'Build completed successfully' in (ROOT/'logs/lake-build.log').read_text()
    assert '\nOK\n' in (ROOT/'logs/storage-tests-venv.log').read_text()
    assert json.loads((ROOT/'logs/negative-replay-seed17.log').read_text())['rejections']==29
    result={'status':'PASS scoped checks; global DocGraph retains 62 known errors','commands':records,'other_checks':existing,'storage':policy,'global_docgraph_exact_base_match':True,'raw_large_new_JSON':large,'authority':'local isolated audit; no commit push PR merge','navigation':'shared source routing reviewed and left at BASE; new independent report only'}
    with (ROOT/'VERIFICATION.json').open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({'status':'PASS','checks':len(records),'global_DocGraph_errors_unchanged':62,'real_index_unchanged':True},sort_keys=True))
if __name__=='__main__':main()
