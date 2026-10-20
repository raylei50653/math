import itertools,json,argparse,hashlib
from collections import Counter
from pathlib import Path
D=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'certificate.json');args=ap.parse_args()
manifest=json.loads((D.parent/'INPUTS.json').read_text())
for item in manifest:
 raw=(D.parent/'frozen'/item['path']).read_bytes()
 assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
rim=('a','b','q','L','u1','u2','n')
inside=('p','h','R')
faces=[('a','b','p'),('b','p','q'),('p','q','h'),('p','h','n'),('p','n','a'),('h','q','L'),('h','L','R'),('h','R','n'),('R','n','u2'),('R','u2','u1'),('R','u1','L')]
vertices=rim+inside
ecount=Counter(tuple(sorted((f[i],f[(i+1)%3]))) for f in faces for i in range(3))
assert {e for e,n in ecount.items() if n==1}=={tuple(sorted((rim[i],rim[(i+1)%7]))) for i in range(7)}
assert all(n in (1,2) for n in ecount.values())
assert len(vertices)-len(ecount)+len(faces)==1
for v,star in (('p',set(('a','b','q','h','n'))),('h',set(('p','q','L','R','n'))),('R',set(('n','h','L','u1','u2')))):
 assert {w for e in ecount if v in e for w in e if w!=v}==star
edges=sorted({tuple(sorted((vertices.index(f[i]),vertices.index(f[(i+1)%3])))) for f in faces for i in range(3)})
def canon(row):
 d={};return tuple(d.setdefault(c,len(d)) for c in row)
rows=sorted({canon(r) for r in itertools.product(range(4),repeat=7) if all(r[i]!=r[(i+1)%7] for i in range(7))})
records=[]
for row in rows:
 lifts=[]
 for inner in itertools.product(range(4),repeat=3):
  c=row+inner
  if all(c[i]!=c[j] for i,j in edges):lifts.append(inner)
 records.append({'rim':list(row),'all_p_h_R_lifts':[list(t) for t in lifts]})
assert len(rows)==91 and sum(bool(r['all_p_h_R_lifts']) for r in records)==31
# all labelled set partitions, retaining only noncrossing ones
parts=[]
def gen(prefix):
 if len(prefix)==7:
  p=tuple(prefix)
  if all(not(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b]) for a,b,c,d in itertools.combinations(range(7),4)):parts.append(p)
  return
 for b in range(1+max(prefix)+1):gen(prefix+[b])
gen([0])
assert len(parts)==429
splits=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
allcols={}
for row in rows:
 splitcols=[]
 for pairs in splits:
  pal={c:i for i,p in enumerate(pairs) for c in p}
  cols=[]
  for p in parts:
   if any(pal[row[i]]!=pal[row[j]] for i in range(7) for j in range(i) if p[i]==p[j]):continue
   if any(pal[row[i]]==pal[row[(i+1)%7]] and p[i]!=p[(i+1)%7] for i in range(7)):continue
   outs=set()
   for mask in range(1<<(1+max(p))):
    out=[]
    for i,c in enumerate(row):
     pair=pairs[pal[c]]
     out.append(pair[0]+pair[1]-c if mask&(1<<p[i]) else c)
    assert all(out[i]!=out[(i+1)%7] for i in range(7))
    outs.add(canon(out))
   cols.append((p,outs))
  splitcols.append(cols)
 allcols[row]=splitcols
assert sum(len(cs) for ss in allcols.values() for cs in ss)==1785
bad={tuple(r['rim']) for r in records if not r['all_p_h_R_lifts']}
rounds=[]
while True:
 removed=[]
 for row in sorted(bad):
  for si,cols in enumerate(allcols[row]):
   if not any(outs<=bad for p,outs in cols):
    removed.append({'rim':list(row),'split_index':si});break
 if not removed:break
 bad-={tuple(r['rim']) for r in removed};rounds.append(removed)
assert len(bad)==50 and [len(r) for r in rounds]==[8,2]
output={'rim':list(rim),'interior':list(inside),'faces':[list(f) for f in faces],'edges':[[vertices[i],vertices[j]] for i,j in edges],'records':records,'noncrossing_partitions':len(parts),'kempe_column_count':sum(len(cs) for ss in allcols.values() for cs in ss),'D_closure_removed_rounds':rounds,'D_consistent_remainder':[list(t) for t in sorted(bad)],'sealed_inputs':len(manifest),'scope':'Complete exact original patch relation and necessary all-noncrossing Kempe model only; no source realization, source exclusion or smaller disk' }
if args.build:
 with args.certificate.open('x') as f:json.dump(output,f,indent=2,sort_keys=True);f.write('\n')
else:assert json.loads(args.certificate.read_text())==output
print(json.dumps({'status':'PASS','proper_C7_orbits':91,'nonempty_complete_lifts':31,'empty_complete_lifts':60,'D_model_remainder':50,'sealed_inputs':len(manifest),'source_excluded':False,'smaller_bad_constructed':False},sort_keys=True))
