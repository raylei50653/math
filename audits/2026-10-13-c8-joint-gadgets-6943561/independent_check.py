"""Independent whole-domain count verification; no producer imports."""
import argparse
import gzip
import itertools
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def normalize(row):
    distinct = list(dict.fromkeys(row))
    return tuple(distinct.index(c) for c in row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    rows = sorted({normalize(p) for p in itertools.product(range(4), repeat=8)
                   if all(p[i] != p[(i+1)%8] for i in range(8))})
    frozen = HERE/'frozen/audits'
    assert rows == list(map(tuple,json.loads((frozen/'2026-10-13-c8-joint-count-3097ef5/interface.json').read_text())['pattern_order']))
    queries = [q for q in json.loads((frozen/'2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json').read_text())['queries'] if q['status']=='necessary_condition_residual']
    expected = json.loads((HERE/'search/RESULTS.json').read_text())
    index = {p:i for i,p in enumerate(rows)}
    transformations=[]
    for sign in [1,-1]:
        for shift in range(8):
            # Inverse permutation directly reads the color at each query pin.
            transformations.append([index[normalize([p[(sign*(i-shift))%8] for i in range(8)])] for p in rows])
    cfg = '\n'.join(' '.join(map(str,r)) for r in rows+transformations+[
        [(q['support']>>i)&1 for i in range(274)] for q in queries])+'\n'
    result=[]
    with tempfile.TemporaryDirectory(prefix='c8-independent-') as td:
        tmp=Path(td);(tmp/'config').write_text(cfg)
        subprocess.run(['g++','-O3','-std=c++17',str(HERE/'independent.cpp'),'-o',str(tmp/'verify')],check=True)
        for h in range(6):
            for name,short in [(f'h{h}.ascii.gz','graphs'),(f'h{h}.counts.u16le.gz','counts'),(f'h{h}.tuples.u16le.gz','tuples')]:
                (tmp/short).write_bytes(gzip.decompress((HERE/'search/data'/name).read_bytes()))
            command=[str(tmp/'verify'),str(tmp/'config'),str(tmp/'graphs'),str(tmp/'counts'),str(tmp/'tuples'),str(tmp/'result')]
            subprocess.run(command,check=True)
            got=json.loads((tmp/'result').read_text());want=expected['by_private_vertices'][h]
            for field in ['graphs','fibres','empty_fibres','full_lifts']:assert got[field]==want[field]
            assert got['minimum_intersections']==[q['minimum_intersection'] for q in want['queries']]
            result.append(got)
            if args.negative and h==0:
                with (tmp/'counts').open('r+b') as f:
                    byte=f.read(1);f.seek(0);f.write(bytes([byte[0]^1]))
                bad=subprocess.run(command,capture_output=True,text=True)
                assert bad.returncode!=0 and 'count mismatch' in bad.stderr
                with (tmp/'counts').open('r+b') as f:f.write(byte)
                with (tmp/'tuples').open('r+b') as f:
                    tuple_byte=f.read(1);f.seek(0);f.write(bytes([tuple_byte[0]^1]))
                bad=subprocess.run(command,capture_output=True,text=True)
                assert bad.returncode!=0 and 'tuple mismatch' in bad.stderr
        print(json.dumps(dict(status='PASS',algorithm='sum proper private assignments by boundary bitsets',by_private_vertices=result,
                              corrupted_fibre_rejected=args.negative,corrupted_tuple_rejected=args.negative),sort_keys=True))


if __name__=='__main__':main()
