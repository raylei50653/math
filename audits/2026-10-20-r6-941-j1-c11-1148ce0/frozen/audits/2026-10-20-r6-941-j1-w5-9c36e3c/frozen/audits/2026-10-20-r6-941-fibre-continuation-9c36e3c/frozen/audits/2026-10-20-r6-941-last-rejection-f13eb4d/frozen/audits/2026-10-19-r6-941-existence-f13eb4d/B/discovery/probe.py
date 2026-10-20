import importlib.util,json,gzip,time
from pathlib import Path
from itertools import product
from math import factorial
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parent/'frozen'
def load(p,name):
 sp=importlib.util.spec_from_file_location(name,ROOT/p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
m=load('audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py','m')
a=load('audits/2026-10-19-r6-941-chains-13dc5ff/C/check.py','a')
cert=json.loads(gzip.decompress((ROOT/'audits/2026-10-19-r6-941-chains-13dc5ff/C/certificate.json.gz').read_bytes()))
ten=[tuple(t) for t in cert['core_states']];C=cert['original_matrix'];Ns=cert['candidate_matrices'];K=m.kempe(10,ten)
Q=[[[0]*len(ten) for _ in range(10)] for j in range(2)]
for i,word in enumerate(ten):
 f=dict(zip(a.PINS,word));b=f['n']
 for c in range(4):
  if c in (f['q'],f['u'],f['s']) or b in (f['a'],c,f['q']):continue
  for x,y,r in product(range(4),repeat=3):
   ff=dict(f,c=c,b=b,x=x,y=y,r=r)
   if x==c or not all(ff[j]!=ff[k] for j,k in a.RIGHT):continue
   row=m.ROWS.index(''.join(map(str,m.canonical((x,y,f['a'],b,c)))))
   for j,flag in enumerate((f['R']==f['q'],f['L']==b)):
    if flag:Q[j][row][i]+=1
 fac=factorial(4-len(set(word)))
 for N in Q:
  for row in N:assert row[i]%fac==0;row[i]//=fac
catalogue=sorted(map(int,json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())['cells']))
for rec in cert['joint_comparisons']:
 if not rec['not_excluded_by_zero_closure']:continue
 lives=rec['live'];zb=rec['zero_bits']
 print('TYPE',zb,'live',len(lives),'Q uppers',[a.projection(m,N,lives) for N in Q],flush=True)
 for j in range(2):
  ll,rs=m.close(K,[i for i in lives if not Q[j][9][i]])
  print(' acceptzero',j+1,len(ll),a.projection(m,C,ll),[a.projection(m,N,ll) for N in Q],[a.projection(m,N,ll) for N in Ns],flush=True)
 for j in range(2):
  ss=[]
  for support in catalogue:
   ll,rs=m.close(K,[i for i in lives if all(not Q[j][r][i] for r in range(10) if not support>>r&1)])
   if a.projection(m,C,ll)!=941:continue
   if any(s&~a.projection(m,N,ll) for s,N in zip(rec['exact_supports_hypothesis'],Ns)):continue
   if support&~a.projection(m,Q[j],ll):continue
   ss.append(support)
  print(' Q catalogue',j+1,ss,flush=True)
