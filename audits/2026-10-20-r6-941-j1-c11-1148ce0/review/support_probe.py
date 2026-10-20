#!/usr/bin/env python3
"""Independent complete-row support analysis for frozen C0,C1 caps."""
from pathlib import Path
from itertools import product
import gzip, json
D=Path(__file__).resolve().parent
A=D.parent/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c'
I=json.load(gzip.open(A/'interface/certificate-v4.json.gz','rt'))
CAT=A/'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen/audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json'
MASKS=sorted(set(map(int,json.loads(CAT.read_text())['cells'])))
NAMES=('a','n','u2','u1','L','q','c','s','v','w','t')
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
RIGHT=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','s'),('r','v'),('r','w'),('r','t'))
def canon(t):
 d={};return tuple(d.setdefault(v,len(d)) for v in t)
def independent_matrices():
 mats=[[[0]*len(I['caps']) for _ in ROWS] for _ in range(2)]
 for i,cap in enumerate(I['caps']):
  c=dict(zip(NAMES,cap['core']))
  right=[]
  for x,y,r in product(range(4),repeat=3):
   cc=c|{'x':x,'y':y,'r':r}
   if all(cc[u]!=cc[v] for u,v in RIGHT):right.append((x,y,r))
  assert right==[tuple(v) for v in cap['right_xyr']]
  for k,u in enumerate(('u1','u2')):
   if c['a']!=c[u] or c['L'] in (c['a'],c['c'],c['q']):continue
   for x,y,r in right:
    row=''.join(map(str,canon((x,y,c['a'],c['L'],c['c']))))
    mats[k][ROWS.index(row)][i]+=1
 return mats

def main():
 mats=independent_matrices();live=set(I['live']);out=[]
 for k in range(2):
  supports=[{i for i in live if m[i]} for m in mats[k]]
  mask=sum(1<<j for j,s in enumerate(supports) if s)
  out.append({'candidate':f'C{k}','maximal_live_support':mask,'is_K132':mask in MASKS,'row_sizes':{r:len(s) for r,s in zip(ROWS,supports)},'all_cell_coefficients_zero_or_one':all(v in (0,1) for row in mats[k] for v in row)})
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
