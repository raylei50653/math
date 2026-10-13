#!/usr/bin/env python3
"""Complete fixed-frame m=9 source controls; no graph-generation premise."""
from pathlib import Path
import argparse
import gzip
import hashlib
import itertools
import json

ROOT = Path(__file__).resolve().parent
ROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
QUERIES = (
    ('c15-933',(0,1,2,0,0),933), ('c18-933',(0,2,1,0,0),933),
    ('c04-941',(0,0,1,0,2),941), ('c07-941',(0,0,2,0,1),941),
    ('c15-941',(0,1,2,0,0),941), ('c18-941',(0,2,1,0,0),941),
    ('c20-941',(1,0,0,0,2),941), ('c30-941',(2,0,0,0,1),941),
)

def graph(e):
    boundary = [f'b{i}' for i in range(5)]
    collar = ['a0']
    for i in range(1,5):
        collar += [f'y{i}_{j}' for j in range(1,e[i]+1)] + [f'a{i}']
    collar += [f'y0_{j}' for j in range(1,e[0]+1)]
    inner = [f't{i}' for i in range(8)]
    vertices = boundary + collar + inner + ['r']
    edges = set()
    faces = []
    def edge(a,b):
        edges.add(tuple(sorted((a,b))))
    def face(a,b,c):
        faces.append((a,b,c))
        edge(a,b); edge(b,c); edge(c,a)
    for i in range(5):
        face(f'b{i}',f'b{(i+1)%5}',f'a{i}')
        fan=[f'a{(i-1)%5}']+[f'y{i}_{j}' for j in range(1,e[i]+1)]+[f'a{i}']
        for a,b in zip(fan,fan[1:]):
            face(f'b{i}',b,a)
    for i in range(8):
        face(collar[i],collar[(i+1)%8],inner[i])
        face(collar[i],inner[i],inner[(i-1)%8])
        face(inner[i],inner[(i+1)%8],'r')
    adj={v:set() for v in vertices}
    for a,b in edges:
        adj[a].add(b);adj[b].add(a)
    assert len(edges)==3*17+2*5-3 == 58
    assert len(vertices)-len(edges)+len(faces)==1
    assert all(len(adj[f'b{i}'])==4+e[i] for i in range(5))
    assert all(len(adj[t])==5 for t in inner)
    assert len(adj['r'])==8
    # Every face is coherently oriented. The outer cycle is the only boundary.
    darts={}
    for f in faces:
        for a,b in zip(f,f[1:]+f[:1]):
            darts[(a,b)]=darts.get((a,b),0)+1
    assert max(darts.values())==1
    assert all(darts.get((a,b),0)+darts.get((b,a),0)==(1 if a in boundary and b in boundary else 2) for a,b in edges)
    return vertices,collar,sorted(edges),faces,adj

def lifts(vertices,adj,row):
    colors={f'b{i}':int(c) for i,c in enumerate(row)}
    result=[]
    def visit():
        if len(colors)==len(vertices):
            result.append(''.join(str(colors[v]) for v in vertices));return
        candidates=[]
        for index,v in enumerate(vertices):
            if v in colors: continue
            legal=tuple(c for c in range(4) if all(colors.get(w)!=c for w in adj[v]))
            candidates.append((len(legal),-sum(w in colors for w in adj[v]),index,v,legal))
        _,_,_,v,legal=min(candidates)
        for c in legal:
            colors[v]=c;visit();del colors[v]
    visit()
    return sorted(result)

def calculate():
    # Exhaustive eight-point combinatorial subclaim, separate from cap topology.
    subsets=[]
    for mask in range(256):
        s=[i for i in range(8) if mask>>i&1]
        if all(min((a-b)%8,(b-a)%8) not in (2,3) for a,b in itertools.combinations(s,2)):
            subsets.append(s)
    assert max(map(len,subsets))==2
    cases=[]
    for name,e,target in QUERIES:
        vertices,collar,edges,faces,adj=graph(e)
        fibres={row:lifts(vertices,adj,row) for row in ROWS}
        counts=[len(fibres[row]) for row in ROWS]
        sigma=sum(1<<i for i,c in enumerate(counts) if c)
        assert sigma==1023 and sigma!=target
        cases.append({'id':name,'e':e,'target':target,'vertices':vertices,'outer_B':vertices[:5],
                      'collar_C':collar,'edges':edges,'oriented_inner_faces':faces,
                      'row_order':ROWS,'counts':counts,'sigma':sigma,'complete_fibres':fibres})
    return {'base':'6cafdfb02fe5892a49eee21f92aea2369a25c022',
            'status':'finite complete m=9 control after paper uniqueness reduction',
            'target_source_status':'not triggered',
            'admissible_C_neighbor_subsets':subsets,'cases':cases}

def frozen_check():
    manifest=json.loads((ROOT/'INPUTS.json').read_text())
    for name,entry in manifest['inputs'].items():
        data=gzip.decompress((ROOT/entry['frozen']).read_bytes())
        assert hashlib.sha256(data).hexdigest()==entry['sha256'],name

def validate(data):
    frozen_check()
    expected=calculate()
    assert data==json.loads(json.dumps(expected)), 'complete source or fibre mismatch'

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true')
    p.add_argument('--negative',action='store_true');args=p.parse_args()
    path=ROOT/'certificate.json.gz'
    if args.write:
        with path.open('xb') as f:f.write(gzip.compress((json.dumps(calculate(),sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
    data=json.loads(gzip.decompress(path.read_bytes()))
    validate(data)
    if args.negative:
        damaged=json.loads(json.dumps(data));damaged['cases'][0]['complete_fibres']['01012'].pop()
        try:validate(damaged)
        except AssertionError:pass
        else:raise AssertionError('deleted full lift was accepted')
    print(json.dumps({'cases':[{k:c[k] for k in ('id','counts','sigma')} for c in data['cases']],
                      'frozen_inputs':'pass','complete_fibre_replay':'pass','negative_control':args.negative},sort_keys=True))

if __name__=='__main__':main()
