#!/usr/bin/env python3
"""Same-source complete-fibre C5 -> C4 cap projection. No source search."""
from collections import Counter
from hashlib import sha256
from itertools import product, permutations
from pathlib import Path
import argparse
import json

PACKAGE=Path(__file__).resolve().parents[1]
CAT=PACKAGE/'frozen/artifacts/c5_cells/cells.json'
OUT=Path(__file__).with_name('certificate.json')
parser=argparse.ArgumentParser()
parser.add_argument('--check', action='store_true', help='Replay without writing outputs')
args=parser.parse_args()
manifest=json.loads((PACKAGE/'INPUTS.json').read_text())
for item in manifest['files']:
    path=PACKAGE/'frozen'/item['path']
    assert sha256(path.read_bytes()).hexdigest()==item['sha256'], item['path']
data=json.loads(CAT.read_text())
REPS=[tuple(x) for x in data['pattern_order']]
QREPS=[(0,1,0,1),(0,1,0,2),(0,1,2,1),(0,1,2,3)]
CY={tuple(sorted((i,(i+1)%5))) for i in range(5)}
PERMS=list(permutations(range(4)))
def norm(b):
    d={}
    return tuple(d.setdefault(c,len(d)) for c in b)
INDEX={b:i for i,b in enumerate(REPS)}
def xy(b):
    if len(set(b))==3:
        return 'y'+str(next(i for i in range(5) if b.count(b[i])==1))
    return 'x'+''.join(str(i) for i in range(5) if b.count(b[i])==2)
NAMES=[xy(b) for b in REPS]

def matrix(j=3, spokes=None):
    if spokes is None: spokes=set(range(5))-{j}
    rows=[]
    for q in QREPS:
        row=[0]*10
        for b in product(range(4), repeat=5):
            if any(b[u]==b[v] for u,v in CY): continue
            if (q[0],b[(j-1)%5],b[j],b[(j+1)%5])!=q: continue
            if any(q[0]==b[i] for i in spokes): continue
            row[INDEX[norm(b)]]+=1
        rows.append(row)
    return rows
M=matrix()
expected=[{'x24':2},{'y3':1,'x02':1,'x14':1},{'y0':1,'y1':1},{'y2':1,'y3':1,'y4':1}]
assert [{NAMES[i]:x for i,x in enumerate(r) if x} for r in M]==expected

def fibres(n,edges,pins):
    adj=[set() for _ in range(n)]
    for u,v in edges: adj[u].add(v);adj[v].add(u)
    c=[-1]*n
    for v,x in pins.items(): c[v]=x
    if any(c[u]>=0 and c[u]==c[v] for u,v in edges): return set()
    out=set()
    def visit():
        rest=[v for v in range(n) if c[v]<0]
        if not rest: out.add(tuple(c));return
        avail={v:set(range(4))-{c[w] for w in adj[v]} for v in rest}
        v=min(rest,key=lambda v:(len(avail[v]),-len(adj[v]),v))
        for x in sorted(avail[v]):
            c[v]=x;visit();c[v]=-1
    visit()
    return out

def mult(M,v): return [sum(a*b for a,b in zip(row,v)) for row in M]
def support(v):return sum(1<<i for i,x in enumerate(v) if x)
records=[]
comparisons=0
for key,entry in sorted(data['cells'].items(),key=lambda p:int(p[0])):
    n=5+entry['k_eff'];e=CY|{tuple(sorted(t)) for t in entry['edges']}
    fs=[fibres(n,e,dict(enumerate(b))) for b in REPS]
    counts=list(map(len,fs));assert support(counts)==int(key)
    lifted=[set() for _ in QREPS]
    for i,b in enumerate(REPS):
        for p in PERMS:
            bb=tuple(p[x] for x in b)
            for a in set(range(4))-{bb[t] for t in (0,1,2,4)}:
                q=(a,bb[2],bb[3],bb[4])
                if q in QREPS:
                    qi=QREPS.index(q)
                    lifted[qi].update(tuple(p[x] for x in c)+(a,) for c in fs[i])
    h_edges=e|{(i,n) for i in (0,1,2,4)}
    direct=[fibres(n+1,h_edges,{n:q[0],2:q[1],3:q[2],4:q[3]}) for q in QREPS]
    assert direct==lifted,(key,'full fibre mismatch')
    sizes=list(map(len,direct));assert sizes==mult(M,counts),(key,'matrix mismatch')
    assert all(c[:-1] in fibres(n,e,{i:c[i] for i in range(5)}) for f in direct for c in f)
    comparisons+=4
    records.append({'source_mask':int(key),'C5_counts':counts,'C4_counts':sizes,
      'fibre_hashes':[sha256(json.dumps(sorted(f)).encode()).hexdigest() for f in direct]})
abstract=[]
for mask in (932,933,941):
    # t + all admitted fan vectors, each coefficient one.
    v=[int(len(set(b))==4) for b in REPS]
    for i in range(5):
        yi=NAMES.index('y'+str(i))
        if mask>>yi&1:
            fan=[int(all(b[u]!=b[w] for u,w in CY|{(i,(i+2)%5),(i,(i+3)%5)})) for b in REPS]
            v=[a+b for a,b in zip(v,fan)]
    assert support(v)==mask
    out=mult(M,v);assert out[2]==0
    abstract.append({'mask':mask,'count_vector':v,'C4_counts':out,'C4_mask':support(out),'source_realized':False})
assert [x['C4_mask'] for x in abstract]==[3,11,11]
# Exhaust every abstract input support; no realizability claim.
all_masks=[support(mult(M,[(m>>i)&1 for i in range(10)])) for m in range(1024)]
assert all_masks[933]==11 and all_masks[941]==11 and all_masks[932]==3
# Wrong named opening does not keep the same formula.
assert matrix(2)!=M
# Restoring the deleted spoke removes the entire u=b3 fibres.
wrong=matrix(spokes=set(range(5)))
assert wrong[0]==[0]*10 and wrong[1]==[0]*10
assert mult(wrong,abstract[2]['count_vector'])!=abstract[2]['C4_counts']
# Explicit five fans certify the monotone multi-hole premise.
fans=[]
for i in range(5):
    es=CY|{tuple(sorted((i,(i+2)%5))),tuple(sorted((i,(i+3)%5)))}
    f=[int(all(b[u]!=b[v] for u,v in es)) for b in REPS]
    fans.append({'vertex':i,'mask':support(f),'counts':f})
assert fans[4]['mask']&933==fans[4]['mask']
assert fans[2]['mask']&941==fans[2]['mask']
assert fans[4]['mask']&941==fans[4]['mask']
result={'C5_pattern_order':REPS,'C5_names':NAMES,'C4_pattern_order':QREPS,'transfer_matrix':M,
 'formula':expected,'abstract_controls':abstract,'real_graph_controls':records,
 'whole_fibre_comparisons':comparisons,'fan_controls':fans,'all_input_supports':len(all_masks),
 'source_catalogue_sha256':sha256(CAT.read_bytes()).hexdigest(),
 'external_census_replayed':False,'target_source_realized':False,
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
if args.check:
    assert json.loads(OUT.read_text())==json.loads(json.dumps(result)), 'Certificate differs'
else:
    OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'ok':True,'real_sources':len(records),'whole_fibre_comparisons':comparisons,
 'abstract_C4_masks': [row['C4_mask'] for row in abstract], 'matrix_shape':[4,10],
 'all_input_supports':len(all_masks), 'external_census_replayed':False},indent=2))
