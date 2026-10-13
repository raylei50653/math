#!/usr/bin/env python3
"""Independent replay and corruption controls; original evidence is never written."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def run(args):
    env=dict(os.environ,PYTHONHASHSEED='17')
    p=subprocess.run([sys.executable,'-B']+list(map(str,args)),capture_output=True,text=True,env=env)
    return {'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def main():
    results={}
    for name,args,cert in [('representatives',['--check'],'certificate.json.gz'),
                           ('t1',[],'certificate.json.gz'),
                           ('conditional',['--check'],'certificate.json')]:
        base=PARENT/name
        paths=[base/'check.py',base/cert]
        if (base/'summary.json').exists(): paths.append(base/'summary.json')
        if (base/'frozen').exists(): paths.extend(sorted((base/'frozen').rglob('*')))
        paths=[p for p in paths if p.is_file()]
        before={str(p.relative_to(PARENT)):digest(p) for p in paths}
        good=run([base/'check.py']+args)
        assert good['exit_code']==0,good
        with tempfile.TemporaryDirectory(prefix='review-tmp-',dir=HERE) as tmp:
            copy=Path(tmp)/name
            shutil.copytree(base,copy,ignore=shutil.ignore_patterns('review-tmp-*'))
            q=copy/cert
            if cert.endswith('.gz'):
                value=json.loads(gzip.decompress(q.read_bytes()))
                if name=='representatives': value['representative']['rows'][0]['cells'][0]=['0'*12]
                else: value['graphs'][0]['rows'][0]['cells'][0]=[[0]*10]
                q.write_bytes(gzip.compress(json.dumps(value,sort_keys=True,separators=(',',':')).encode(),mtime=0))
            else:
                value=json.loads(q.read_text()); value['proper_rim_assignments_checked']=239
                q.write_text(json.dumps(value))
            bad=run([copy/'check.py']+args)
            assert bad['exit_code']!=0,bad
        after={str(p.relative_to(PARENT)):digest(p) for p in paths}
        assert before==after
        results[name]={'normal_seed17':good,'corrupted_copy':bad,'original_hashes_unchanged':True,
                       'sha256':after}
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
