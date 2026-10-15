#!/usr/bin/env python3
"""Read-only certificate validation. Coloring witnesses use no search solver.

For residuals or empty-fibre exclusions, exhaustive search is replayed; these
outcomes cannot be validated by a witness for a different row.
"""
import argparse
from collections import Counter
import gzip
import json
from itertools import zip_longest
from pathlib import Path
import search

def validate(rot,frame,result):
    n=len(rot);x,y,a,b,c=frame['B'];r,t,p,q,s=frame['apices']
    omitted={frame['root'],x,y,b,r}
    live=set(range(n))-omitted
    representative=lambda v:a if v==c else v
    vertices={representative(v) for v in live}
    edges={tuple(sorted((representative(v),representative(w)))) for v in live for w in rot[v] if w in live}
    assert all(v!=w for v,w in edges)
    order=result['u_original_order']
    assert len(order)==len(vertices) and set(order)==vertices
    assert order[:7]==[a,s,frame['v'],frame['w'],t,p,q]
    if 'lift' in result:
        lift=result['lift'];assert len(lift)==len(order) and set(lift)<=set('0123')
        color=dict(zip(order,map(int,lift)))
        assert all(color[v]!=color[w] for v,w in edges), 'improper full lift'
        assert lift[:5]==search.WORDS[result['row']]
        if result['outcome']=='forbidden_outer':
            assert result['row'] in (6,7,9)
        else:
            assert result['outcome']=='forbidden_joint'
            # Re-derive the old R constraints in the same literal color frame.
            zc,sc,vc,wc,tc,pc,qc=map(int,lift[:7]);bad=False
            for rc in set(range(4))-{sc,vc,wc,tc}:
                if zc==rc:
                    accepted=sc==tc and {pc,qc}==set(range(4))-{zc,sc}
                elif sc==tc:
                    accepted=bool({pc,qc} & (set(range(4))-{zc,sc,rc,tc}))
                else:
                    accepted={pc,qc}=={sc,tc}
                if not accepted:bad=True
            assert bad, 'all r lifts satisfy source constraints'
    else:
        _,adj=search.make_u(rot,frame)
        assert search.classify(adj)=={k:v for k,v in result.items() if k not in ('frame','u_original_order')}

def replay(input_path,certificate,summary_path):
    counts=Counter();search.seal()
    with search.open_read(input_path) as inp, search.open_read(certificate) as cert:
        for source_line,cert_line in zip_longest(inp,cert):
            assert source_line is not None and cert_line is not None, 'missing sphere'
            source=json.loads(source_line);record=json.loads(cert_line)
            assert source['sphere']==record['sphere']
            assert len(source['frames'])==len(record['results']), 'missing frame'
            for frame,result in zip(source['frames'],record['results'],strict=True):
                assert frame==result['frame'], 'pin/frame mismatch'
                validate(source['rotation'],frame,result)
                counts['frames']+=1;counts['queries']+=result['queries'];counts[result['outcome']]+=1
            counts['spheres']+=1
    summary=json.loads(Path(summary_path).read_text())
    assert dict(counts)==summary['counts'], 'summary coverage mismatch'
    return dict(counts)

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('certificate');p.add_argument('summary');a=p.parse_args()
    print(json.dumps({'status':'PASS exact original-edge witness replay','counts':replay(a.input,a.certificate,a.summary)}))

if __name__=='__main__':main()
