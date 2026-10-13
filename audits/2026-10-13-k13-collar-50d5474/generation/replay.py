#!/usr/bin/env python3
"""Recompile fixed BASE plantri and replay both exhaustive generation routes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
BASE='50d5474f2446403f3b3001d5943571184c8c9936'
SOURCE=REPO/'artifacts/c5_excess_two_independent_search/vendor/plantri.c'
GUIDE=SOURCE.with_name('plantri-guide.txt')
PRODUCTS=['spheres19.pc','spheres19_from_min4.pc','inner_spheres14.pc',
          'spheres19.json','rooted_sources.json','generation_summary.json',
          'min4_to_min5.json','inner_filters.json','inner_cores.json',
          'named_configurations.json','primary_to_inner.json','inner_summary.json']

def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--seed',type=int,default=0)
    args=ap.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if any((out/p).exists() for p in PRODUCTS):raise SystemExit('refusing to overwrite previous mathematical products')
    env=os.environ.copy();env['PYTHONHASHSEED']=str(args.seed);env['PYTHONDONTWRITEBYTECODE']='1'
    logs=[]
    def run(argv,label):
        proc=subprocess.run([str(x) for x in argv],cwd=REPO,env=env,capture_output=True)
        (out/(label+'.stdout.log')).write_bytes(proc.stdout)
        (out/(label+'.stderr.log')).write_bytes(proc.stderr)
        logs.append(dict(label=label,argv=list(map(str,argv)),returncode=proc.returncode))
        if proc.returncode:raise RuntimeError(label)
    for source in (SOURCE,GUIDE):
        frozen=subprocess.check_output(['git','show',f'{BASE}:{source.relative_to(REPO)}'],cwd=REPO)
        assert source.read_bytes()==frozen,source
    with tempfile.TemporaryDirectory(prefix='k13-plantri-') as tmp:
        tmp=Path(tmp);binary=tmp/'plantri';filtered=tmp/'plantri_min4_filter'
        run(['cc','-O3','-std=c11',SOURCE,'-o',binary],'compile')
        run(['cc','-O3','-std=c11',f'-DPLUGIN={HERE / "min5_filter.c"}',SOURCE,'-o',filtered],'compile_filter')
        run([binary,'-m5','19',out/'spheres19.pc'],'min5_19')
        run([filtered,'-m4','19',out/'spheres19_from_min4.pc'],'min4_19_filter')
        run([binary,'-m4','14',out/'inner_spheres14.pc'],'min4_14')
        run([sys.executable,HERE/'generate.py','--directory',out],'parse_sources')
        run([sys.executable,HERE/'inner_cover.py','--directory',out],'inner_cover')
    manifest=dict(base=BASE,seed=args.seed,
        inputs={str(p.relative_to(REPO)):sha(p.read_bytes()) for p in (SOURCE,GUIDE,HERE/'min5_filter.c',HERE/'generate.py',HERE/'inner_cover.py',HERE/'replay.py')},
        products={p:dict(sha256=sha((out/p).read_bytes()),bytes=(out/p).stat().st_size) for p in PRODUCTS},
        commands=logs,
        compiler=subprocess.check_output(['cc','--version'],text=True).splitlines()[0],
        python=sys.version,
        external_page='https://users.cecs.anu.edu.au/~bdm/plantri/',
        external_min5_theorem='https://users.cecs.anu.edu.au/~bdm/plantri/min5paper_sc.pdf',
        external_min4_description='https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf')
    (out/'replay_manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(output=str(out),seed=args.seed,products=len(PRODUCTS))))

if __name__=='__main__':main()
