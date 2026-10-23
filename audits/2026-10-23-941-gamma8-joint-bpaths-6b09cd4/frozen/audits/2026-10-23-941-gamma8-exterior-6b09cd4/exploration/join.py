from itertools import product
from pathlib import Path
from collections import Counter
import json
ROOT=Path(__file__).resolve().parents[3]
OLD=json.loads((ROOT/'audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json').read_text())
ROWS=json.loads((ROOT/'audits/2026-10-23-three-mask-round3-cb8f859/941/certificate.json').read_text())['source_rows']
BOUND=['a','z1','z2','z3','z4','V','U','HL_0','q','c','s','v','w','t']
def edge(a,b):return tuple(sorted((a,b)))
def components(es,co,pair):
 unseen={v for v in co if co[v] in pair};out=[]
 while unseen:
  todo=[min(unseen)];part=set()
  while todo:
   v=todo.pop()
   if v in part:continue
   part.add(v);todo.extend(b if a==v else a for a,b in es if v in (a,b) and co[b if a==v else a] in pair and (b if a==v else a) not in part)
  unseen-=part;out.append(part)
 return out

def refines(es,co,pair,gates):
 parts=[c&set(BOUND) for c in components(es,co,pair)]+[c&set(BOUND) for c in components(es,co,set(range(4))-set(pair))]
 good=[]
 for i,gate in enumerate(gates):
  blocks=[set(b) for b in gate]
  if all(any(p<=b for b in blocks) for p in parts if p):good.append(i)
 return good

def joined(case,row,att,m,n,k):
 mp={v:'g_'+v for v in OLD['original_colors']};mp.update({v:bn for v,bn in zip(['d','e','h','W'],att) if bn})
 co=dict(row['original_boundary_colors'])
 for v,color in OLD['original_colors'].items():co[mp[v]]=color ^ (2 if ((m and OLD['original_component_labels'][v]=='M') or (n and OLD['original_component_labels'][v]=='N') or (k and OLD['original_component_labels'][v]=='K')) else 0)
 if k:co['U']=row['original_boundary_colors']['U'] ^ 2
 es={edge(mp[a],mp[b]) for a,b in case['edges']}|{edge(a,b) for a,b in zip(BOUND,BOUND[1:]+BOUND[:1])}
 return es,co,mp

def gates03(row):
 p=['w','t'] if row['target']==44459 else ['t']
 q=['q','v'] if row['target']==44459 else ['q','w']
 cs=['c','s'] if row['target']==44459 else ['c','s','v']
 return [[['a','z1','z2','z3','z4','U'],['V'],['HL_0']+p,q,cs],[['a','z1','z2','z3','z4'],['V','HL_0']+p,['U'],q,cs]]

def test(case,row,att):
 failures=[]
 for m,n,k in product(range(2),repeat=3):
  es,co,mp=joined(case,row,att,m,n,k)
  if any(co[a]==co[b] for a,b in es):failures.append([m,n,k,'improper']);continue
  if k:
   if not refines(es,co,{0,3},[row['complete_predecessor_record']['full_03_successor_boundary_contacts']]):failures.append([m,n,k,'unique_successor'])
  else:
   if not refines(es,co,{0,3},gates03(row)):failures.append([m,n,k,'initial03'])
   if not refines(es,co,{0,1},row['complete_predecessor_record']['complete_initial_01_gate']):failures.append([m,n,k,'initial01'])
   if not refines(es,co,{0,2},[row['complete_predecessor_record']['complete_initial_02_contacts']]):failures.append([m,n,k,'initial02'])
 es,co,mp=joined(case,row,att,0,0,0)
 neigh=lambda v:{b if a==v else a for a,b in es if v in (a,b)}
 for a,b,allow in [('U','z4',{'V'}),('HL_0','V',{'U'})]:
  if (neigh(a)&neigh(b))-allow:failures.append(['fixed_common_neighbor',a,b])
 return failures

if __name__=='__main__':
 allrows=[]
 for case in OLD['candidates']:
  if case['classification']!='local_necessary_type':continue
  for row in ROWS:
   for att in product([None,'U'],[None,'V','HL_0'],[None,'c'],[None,'q']):
    f=test(case,row,att);allrows.append(dict(case=case['id'],target=row['target'],type02=row['initial_02_type'],attachment=att,failures=f))
 print('rows',len(allrows),'retained',sum(not r['failures'] for r in allrows))
 print('per local',dict(Counter(r['case'] for r in allrows if not r['failures'])))
 print('failed rules',dict(Counter(f[-1] for r in allrows for f in r['failures'])))
 print('surviving attachment counts',dict(Counter(str(r['attachment']) for r in allrows if not r['failures'])))
 for att in product([None,'U'],[None,'V','HL_0'],[None,'c'],[None,'q']):
  cases=sorted({r['case'] for r in allrows if r['attachment']==att and not r['failures']})
  print(att,len(cases),cases)
 with (Path(__file__).parent/'joins.json').open('x') as f:json.dump(allrows,f,indent=2,sort_keys=True);f.write('\n')
