import sys
sys.dont_write_bytecode=True
import importlib.util,json,itertools
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
s=importlib.util.spec_from_file_location('r4',ROOT/'audits/2026-10-23-three-mask-round4-cb8f859/933/check.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
src=json.loads((ROOT/m.SRC).read_text());E=[tuple(t) for t in src['tuples']];ei={t:i for i,t in enumerate(E)};live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933));D=list(m.properwords(10));di={t:i for i,t in enumerate(D)}
bad={j for j,t in enumerate(D) if any(ei[m.canonical(e)] not in live for r,x,y,e in m.complete_cap(t))}
rows=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232');M=[]
for word in rows:
 A,s,v,w,t=map(int,word);row=[0]*len(D)
 for n,R,L,q in itertools.product(range(4),repeat=4):
  d=(A,n,R,L,q,A,s,v,w,t)
  if all(d[i]!=d[(i+1)%10] for i in range(10)):row[di[m.canonical(d)]]+=1
 M.append(row)
 print(word,'terms',sum(row),'allowed ids',[j for j,c in enumerate(row) if c and j not in bad])
print('six Hrows')
for tail in m.TAILS: print(tail,m.canonical((0,)+tail))
with (P/'H-probe.json').open('x') as f:json.dump({'Dzero_count':len(bad),'row_order':rows,'M_H':M,'zero_D':sorted(bad)},f)
print('Hprime = D/(a=R=c)')
M2=[]
for word in rows:
 A,s,v,w,t=map(int,word);row=[0]*len(D)
 for n,L,q in itertools.product(range(4),repeat=3):
  d=(A,n,A,L,q,A,s,v,w,t)
  if all(d[i]!=d[(i+1)%10] for i in range(10)):row[di[m.canonical(d)]]+=1
 M2.append(row)
 print(word,'terms',sum(row),'allowed ids',[j for j,c in enumerate(row) if c and j not in bad])
with (P/'Hprime-probe.json').open('x') as f:json.dump({'Dzero_count':len(bad),'row_order':rows,'M_Hprime':M2},f)
