import itertools,json
from pathlib import Path
D=Path(__file__).resolve().parent
rim=('a','b','q','L','u1','u2','n')
inside=('p','h','R')
faces=[('a','b','p'),('b','p','q'),('p','q','h'),('p','h','n'),('p','n','a'),('h','q','L'),('h','L','R'),('h','R','n'),('R','n','u2'),('R','u2','u1'),('R','u1','L')]
vertices=rim+inside
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
print('row count',len(rows),'extending',sum(bool(r['all_p_h_R_lifts']) for r in records),'empty',sum(not r['all_p_h_R_lifts'] for r in records))
# all labelled set partitions, retaining only noncrossing ones
parts=[]
def gen(prefix):
 if len(prefix)==7:
  p=tuple(prefix)
  if all(not(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b]) for a,b,c,d in itertools.combinations(range(7),4)):parts.append(p)
  return
 for b in range(1+max(prefix)+1):gen(prefix+[b])
gen([0])
print('noncrossing',len(parts))
splits=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
allcols={}
for row in rows:
 splitcols=[]
 for pairs in splits:
  pal={c:i for i,p in enumerate(pairs) for c in p}
  cols=[]
  for p in parts:
   if sum(p[i]!=p[(i+1)%7] for i in range(7))!=2*max(p):continue
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
print('columns',sum(len(cs) for ss in allcols.values() for cs in ss))
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
print('D remainder',len(bad),'rounds',[len(r) for r in rounds])
output={'rim':list(rim),'interior':list(inside),'faces':[list(f) for f in faces],'edges':[[vertices[i],vertices[j]] for i,j in edges],'records':records,'noncrossing_partitions':len(parts),'kempe_column_count':sum(len(cs) for ss in allcols.values() for cs in ss),'D_closure_removed_rounds':rounds,'D_consistent_remainder':[list(t) for t in sorted(bad)]}
p=D/'triangulated-relation-probe.json'
if not p.exists():p.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
else:assert json.loads(p.read_text())==output
