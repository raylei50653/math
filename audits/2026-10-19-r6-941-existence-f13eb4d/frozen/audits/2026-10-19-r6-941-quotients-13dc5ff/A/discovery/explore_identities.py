from pathlib import Path
from fractions import Fraction
import itertools,json,importlib.util
ROOT=Path.cwd(); OLD=ROOT/'audits/2026-10-19-r6-941-leakage-b89c591';spec=importlib.util.spec_from_file_location('model',OLD/'A/model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def rr(a):
 a=[[Fraction(x) for x in r] for r in a];piv=[]
 for col in range(len(a[0])):
  k=next((i for i in range(len(piv),len(a)) if a[i][col]),None)
  if k is None:continue
  r=len(piv);a[r],a[k]=a[k],a[r];q=a[r][col];a[r]=[x/q for x in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][col]:
    q=a[i][col];a[i]=[x-q*y for x,y in zip(a[i],a[r])]
  piv.append(col)
 return a,piv

eight=[t for t in m.growth(8,four=True) if m.proper(t)];i8={t:i for i,t in enumerate(eight)}
parts=[p for p in m.growth(8) if m.proper(p) and m.nc(p)]
A=[[int(all(p[i]!=p[j] or t[i]==t[j] for i in range(8) for j in range(i))) for p in parts] for t in eight]
src=json.loads((ROOT/'audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json').read_text());live=set(next(r for r in src['results'] if r['source_mask']==941)['surviving_ids'])
r,piv=rr([a for i,a in enumerate(A) if i not in live]);free=[i for i in range(len(parts)) if i not in piv];B=[]
for f in free:
 v=[Fraction(0)]*len(parts);v[f]=1
 for k,p in enumerate(piv):v[p]=-r[k][f]
 B.append([sum(x*y for x,y in zip(a,v)) for a in A])
M={n:[[0]*274 for _ in range(10)] for n in ('G','Q1','Q2','GB')};aa=[0]*274
for j,row in enumerate(m.ROWS):
 x,y,a,b,c=map(int,row)
 for n,R,L,q in itertools.product(range(4),repeat=4):
  t=(a,n,R,L,q,c,x,y)
  if not m.proper(t) or b in {a,c,q}:continue
  i=i8[m.canonical(t)];ls=[(p,h) for p,h in itertools.product(range(4),repeat=2) if p not in {a,b,q,n,h} and h not in {p,q,L,R,n}]
  M['G'][j][i]+=len(ls)
  M['Q1'][j][i]+=int(n==b and R==q);M['Q2'][j][i]+=int(n==b and L==b);M['GB'][j][i]+=int(b not in {n,R,L})
  if j==9:aa[i]+=sum(h==a for p,h in ls)

def test(name,v):
 vals=[sum(x*y for x,y in zip(v,b)) for b in B];print(name,all(x==0 for x in vals),sorted(set(vals)),flush=True)
def lin(*pairs):return [sum(c*v[i] for c,v in pairs) for i in range(274)]
print('basis',len(B))
for n in ('Q1','Q2'):
 test(n+'T=GB T',lin((1,M[n][1]),(-1,M['GB'][1])))
 test(n+'V=T+U',lin((1,M[n][6]),(-1,M[n][1]),(-1,M[n][4])))
test('U1+U2=Aa/2',lin((2,M['Q1'][4]),(2,M['Q2'][4]),(-1,aa)))
test('T1=T2',lin((1,M['Q1'][1]),(-1,M['Q2'][1])))
# All exact count relations among acceptance/rejection/sectors.
names=['a1','a2','T1','U1','V1','T2','U2','V2','Tg','Ug','Vg','Aa','Ag']
vecs=[M['Q1'][9],M['Q2'][9],M['Q1'][1],M['Q1'][4],M['Q1'][6],M['Q2'][1],M['Q2'][4],M['Q2'][6],M['GB'][1],M['GB'][4],M['GB'][6],aa,M['G'][9]]
Z=[[sum(x*y for x,y in zip(v,b)) for v in vecs] for b in B];z,p=rr(Z)
for f in range(len(names)):
 if f in p:continue
 v=[Fraction(0)]*len(names);v[f]=1
 for k,j in enumerate(p):v[j]=-z[k][f]
 print('relation',[(names[i],str(c)) for i,c in enumerate(v) if c])
cone=json.loads((ROOT/'audits/2026-10-18-smaller-bad-counts-e1617a2/A/cone-triangulated.json').read_text());rows=cone['rows'];allowed=[col for col in cone['columns'] if all(rows[r]['tuple_id'] in live for r,v in col['entries'])];sz=[0]*274
for r in rows:sz[r['tuple_id']]+=r['orbit_size']
for name,v in [('T1=T2',lin((1,M['Q1'][1]),(-1,M['Q2'][1]))),('T1=Tg',lin((1,M['Q1'][1]),(-1,M['GB'][1]))),('V1=T1+U1',lin((1,M['Q1'][6]),(-1,M['Q1'][1]),(-1,M['Q1'][4]))),('2U1+2U2=Aa',lin((2,M['Q1'][4]),(2,M['Q2'][4]),(-1,aa)))]:
 vals=[sum(Fraction(v[rows[r]['tuple_id']],sz[rows[r]['tuple_id']])*n for r,n in c['entries']) for c in allowed]
 print('ORBIT-Average',name,all(x==0 for x in vals),sorted(set(vals)))
from collections import defaultdict
blocks=defaultdict(list)
for j,r in enumerate(rows):
 side=tuple(c//2 for c in r['tuple']);key=min(side,tuple(1-c for c in side));blocks[key].append(j)
linear=[]
for key,ri in blocks.items():
 rowmap={r:i for i,r in enumerate(ri)}
 columns=[]
 for c in allowed:
  if c['entries'][0][0] not in rowmap:continue
  assert all(r in rowmap for r,v in c['entries'])
  v=[0]*len(ri)
  for r,n in c['entries']:v[rowmap[r]]=n
  columns.append(v)
 if columns:
  r,p=rr(columns)
 else:r=[];p=[]
 for f in range(len(ri)):
  if f in p:continue
  y=[Fraction(0)]*len(ri);y[f]=1
  for k,j in enumerate(p):y[j]=-r[k][f]
  eqn=[Fraction(0)]*274
  for j,v in enumerate(y):
   row=rows[ri[j]];eqn[row['tuple_id']]+=v*row['orbit_size']
  if any(eqn):linear.append(eqn)
print('counted derived rows',len(linear),flush=True)
# Restrict signed planar coefficients to both support and counted linear equations.
Aeq=[[sum(x*y for x,y in zip(v,col)) for col in zip(*A)] for v in linear]
Aeq += [a for i,a in enumerate(A) if i not in live]
r,p=rr(Aeq);free=[i for i in range(len(parts)) if i not in p];BC=[]
for f in free:
 v=[Fraction(0)]*len(parts);v[f]=1
 for k,j in enumerate(p):v[j]=-r[k][f]
 BC.append([sum(x*y for x,y in zip(a,v)) for a in A])
print('counted+span basis',len(BC),flush=True)
for name,v in [('T1=T2',lin((1,M['Q1'][1]),(-1,M['Q2'][1]))),('T1=Tg',lin((1,M['Q1'][1]),(-1,M['GB'][1]))),('V1=T1+U1',lin((1,M['Q1'][6]),(-1,M['Q1'][1]),(-1,M['Q1'][4]))),('V2=T2+U2',lin((1,M['Q2'][6]),(-1,M['Q2'][1]),(-1,M['Q2'][4]))),('2U1+2U2=Aa',lin((2,M['Q1'][4]),(2,M['Q2'][4]),(-1,aa)))]:
 vals=[sum(x*y for x,y in zip(v,b)) for b in BC];print('COUNTED+SPAN',name,all(x==0 for x in vals),sorted(set(vals)),flush=True)
