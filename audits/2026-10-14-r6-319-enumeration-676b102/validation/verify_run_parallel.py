#!/usr/bin/env python3
"""Full read-only partition/receipt/certificate integrity and witness replay."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import json
from pathlib import Path
import sys
import subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import search
import replay

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('n',type=int);a=p.parse_args();h=search.HERE
    d=h/'runs'/f'n{a.n}';s=json.loads((d/'SUMMARY.json').read_text());search.seal()
    assert s['input_seal_sha256']==search.seal()
    for name,digest in s['source_sha256'].items():assert sha(h/name)==digest,name
    assert s['parts_completed']==list(range(s['parts']))
    expected={29:4412031,30:16248772}[a.n]
    def part(i):
        prefix=d/f'{i:03d}';r=json.loads(Path(str(prefix)+'.receipt.json').read_text())
        assert (r['n'],r['part'],r['parts'])==(a.n,i,s['parts'])
        assert r['generation_command'][-4:]==['-m5','-u',str(a.n),f'{i}/{s["parts"]}']
        inp=Path(str(prefix)+'.input.jsonl.gz');cert=Path(str(prefix)+'.certificate.jsonl.gz')
        assert sha(inp)==r['input_sha256'] and sha(cert)==r['certificate_sha256']
        checked=subprocess.run([sys.executable,'-B',str(h/'src/replay.py'),str(inp),str(cert),str(cert)+'.summary.json'],capture_output=True,text=True,check=True)
        count=json.loads(checked.stdout)['counts']
        assert count==r['search']['counts']
        assert r['generation_counts']['seven_pin_edges']==count.get('frames',0)
        assert r['generation_counts']['emitted_spheres']==count.get('spheres',0)
        return r['generation_counts'],count
    gen=Counter();color=Counter()
    with ThreadPoolExecutor(max_workers=8) as pool:
        for future in as_completed([pool.submit(part,i) for i in range(s['parts'])]):
            g,c=future.result();gen.update(g);color.update(c)
    assert dict(gen)==s['generation_counts'] and gen['spheres']==expected
    assert dict(color)==s['search_counts']
    print(json.dumps({'status':'PASS all partitions, hashes, original-edge full witnesses','n':a.n,'k':a.n-6,'counts':dict(color),'spheres_generated':gen['spheres']}),flush=True)

if __name__=='__main__':main()
