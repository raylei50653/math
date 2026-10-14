#!/usr/bin/env python3
"""Complete split generation and witness production; exclusive run directory."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import search

EXPECTED={29:4412031,30:16248772}

def digest(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('n',type=int,choices=sorted(EXPECTED));p.add_argument('--parts',type=int,default=32);p.add_argument('--workers',type=int,default=8);a=p.parse_args()
    h=search.HERE;directory=h/'runs'/f'n{a.n}';directory.mkdir(exist_ok=False)
    code={str(f.relative_to(h)):digest(f) for f in (h/'src').iterdir() if f.is_file()}
    started=time.monotonic();search.seal()
    def job(i):
        prefix=directory/f'{i:03d}';inp=Path(str(prefix)+'.input.jsonl.gz');cert=Path(str(prefix)+'.certificate.jsonl.gz')
        cmd=[str(h/'src/r6-filter'),'-m5','-u',str(a.n),f'{i}/{a.parts}']
        before=time.monotonic();err=Path(str(prefix)+'.generation.stderr')
        with err.open('xb') as es, gzip.open(inp,'xb',compresslevel=6) as out:
            proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=es)
            shutil.copyfileobj(proc.stdout,out);proc.stdout.close();ret=proc.wait()
        assert ret==0,(i,ret)
        generation=time.monotonic()-before
        text=err.read_text();counts=json.loads(next(s.removeprefix('R6_COUNTS ') for s in text.splitlines() if s.startswith('R6_COUNTS ')))
        cmd2=['python3','-B',str(h/'src/search.py'),'audit',str(inp),str(cert)]
        with Path(str(prefix)+'.search.stdout').open('xb') as out,Path(str(prefix)+'.search.stderr').open('xb') as es:
            subprocess.run(cmd2,stdout=out,stderr=es,check=True)
        summary=json.loads(Path(str(cert)+'.summary.json').read_text())
        assert counts['seven_pin_edges']==summary['counts'].get('frames',0)
        assert counts['emitted_spheres']==summary['counts'].get('spheres',0)
        rec={'part':i,'parts':a.parts,'n':a.n,'generation_command':cmd,'search_command':cmd2,
             'generation_elapsed':generation,'generation_counts':counts,'search':summary,
             'input_sha256':digest(inp),'certificate_sha256':digest(cert),'elapsed':time.monotonic()-before}
        Path(str(prefix)+'.receipt.json').write_text(json.dumps(rec,indent=2)+'\n')
        return rec
    records=[]
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        futures=[pool.submit(job,i) for i in range(a.parts)]
        for f in as_completed(futures):
            rec=f.result();records.append(rec)
            print(json.dumps({'done':len(records),'parts':a.parts,'part':rec['part'],'frames':rec['search']['counts'].get('frames',0),'elapsed':round(time.monotonic()-started,2)}),flush=True)
    assert len(records)==a.parts and {r['part'] for r in records}==set(range(a.parts))
    from collections import Counter
    gen=Counter();results=Counter()
    for r in records:gen.update(r['generation_counts']);results.update(r['search']['counts'])
    assert gen['spheres']==EXPECTED[a.n]
    assert code=={str(f.relative_to(h)):digest(f) for f in (h/'src').iterdir() if f.is_file()}, 'source changed during run'
    summary={'n':a.n,'k':a.n-6,'parts':a.parts,'workers':a.workers,'generation_counts':dict(gen),
             'search_counts':dict(results),'elapsed':time.monotonic()-started,'source_sha256':code,
             'input_seal_sha256':search.seal(),'parts_completed':sorted(r['part'] for r in records),
             'scope':'complete minimum-degree-five sphere generation; all roots and ten frames; named r6 necessary source filters; no general K bound'}
    (directory/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
