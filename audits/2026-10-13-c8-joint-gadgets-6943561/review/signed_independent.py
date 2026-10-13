#!/usr/bin/env python3
"""Independent all-signed-fibres replay; no producer imports."""
import argparse
import gzip
import itertools
import json
from pathlib import Path
import subprocess
import tempfile
import time
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent


def normalize(row):
    names=list(dict.fromkeys(row));return tuple(names.index(c) for c in row)


def main():
    p=argparse.ArgumentParser();p.add_argument('--negative',action='store_true');p.add_argument('--output',type=Path,default=HERE/'SIGNED_VERIFICATION.json');args=p.parse_args()
    rows=sorted({normalize(p) for p in itertools.product(range(4),repeat=8) if all(p[i]!=p[(i+1)%8] for i in range(8))})
    frozen=AUDIT/'frozen/audits'
    assert rows==list(map(tuple,json.loads((frozen/'2026-10-13-c8-joint-count-3097ef5/interface.json').read_text())['pattern_order']))
    queries=[q for q in json.loads((frozen/'2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json').read_text())['queries'] if q['status']=='necessary_condition_residual']
    index={p:i for i,p in enumerate(rows)}
    transformations=[[index[normalize([p[(sign*(i-shift))%8] for i in range(8)])] for p in rows] for sign in [1,-1] for shift in range(8)]
    config='\n'.join(' '.join(map(str,r)) for r in rows+transformations+[[(q['support']>>i)&1 for i in range(274)] for q in queries])+'\n'
    result=[];start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='c8-signed-independent-') as td:
        tmp=Path(td);(tmp/'config').write_text(config)
        subprocess.run(['g++','-O3','-std=c++17',str(HERE/'signed_independent.cpp'),'-o',str(tmp/'verify')],check=True)
        for h in range(6):
            files=[(AUDIT/f'search/data/h{h}.ascii.gz','graphs')]+[(AUDIT/f'search/signed_data/h{h}.{name}.gz',short) for name,short in [('counts.u16le','counts'),('tuples.u16le','tuples'),('signatures.u8','signatures')]]
            for path,short in files:
                # Enables independent verification while producer finishes h=5.
                for _ in range(600):
                    if path.exists():break
                    time.sleep(1)
                assert path.exists(),path
                (tmp/short).write_bytes(gzip.decompress(path.read_bytes()))
            command=[str(tmp/'verify')]+[str(tmp/x) for x in ['config','graphs','counts','tuples','signatures','result']]
            subprocess.run(command,check=True)
            got=json.loads((tmp/'result').read_text())
            lines=[json.loads(line) for line in (AUDIT/f'search/signed_h{h}.jsonl').read_text().splitlines()]
            want=next(q for q in lines if q['kind']=='summary')
            for field in ['graphs','valid_signed_graphs','rejections','minimum_intersections','forced_rows']:assert got[field]==want[field],(h,field,got[field],want[field])
            assert got['full_lifts']==want['full_lifts_ignoring_chords']
            assert got['empty_signed_fibres']==(got['valid_signed_graphs']-got['graphs'])*274+want['empty_fibres_ignoring_chords']
            assert got['cap_query_checks']==got['valid_signed_graphs']*16*8
            got['private_vertices']=h;result.append(got)
            print(json.dumps(got),flush=True)
            if args.negative and h==0:
                for filename,message in [('counts','count mismatch'),('tuples','tuple mismatch'),('signatures','signature mismatch')]:
                    with (tmp/filename).open('r+b') as f:byte=f.read(1);f.seek(0);f.write(bytes([byte[0]^1]))
                    bad=subprocess.run(command,capture_output=True,text=True)
                    assert bad.returncode!=0 and message in bad.stderr,(filename,bad.stderr)
                    with (tmp/filename).open('r+b') as f:f.write(byte)
    expected=json.loads((AUDIT/'search/SIGNED_RESULTS.json').read_text())
    assert sum(r['graphs'] for r in result)==expected['graphs']
    assert sum(r['valid_signed_graphs'] for r in result)==expected['valid_signed_graphs']
    assert sum(r['rejections'] for r in result)==expected['rejections']==0
    assert [min(r['minimum_intersections'][i] for r in result) for i in range(8)]==[expected['minimum_intersections'][q['query_id']] for q in queries]
    receipt={'status':'PASS','algorithm':'exhaustive private assignments + boundary bitsets + equality transitive closure',
        'by_private_vertices':result,'negative_controls_rejected':3 if args.negative else 0,
        'elapsed_seconds':round(time.monotonic()-start,3),'graphs':sum(r['graphs'] for r in result),
        'valid_signed_graphs':sum(r['valid_signed_graphs'] for r in result),
        'signed_fibres':sum(r['signed_fibres'] for r in result),'full_lifts':sum(r['full_lifts'] for r in result),
        'empty_signed_fibres':sum(r['empty_signed_fibres'] for r in result),
        'cap_query_checks':sum(r['cap_query_checks'] for r in result),
        'forced_rows':{q['query_id']:sorted(set().union(*(set(r['forced_rows'][i]) for r in result))) for i,q in enumerate(queries)}}
    args.output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','graphs':receipt['graphs'],'valid_signed_graphs':receipt['valid_signed_graphs'],'elapsed_seconds':receipt['elapsed_seconds']}))

if __name__=='__main__':main()
