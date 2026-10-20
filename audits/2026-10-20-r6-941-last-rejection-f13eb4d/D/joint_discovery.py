import importlib.util,json,time
from pathlib import Path
D=Path(__file__).resolve().parent;F=D.parent/'frozen';OLD=F/'audits/2026-10-19-r6-941-existence-f13eb4d'
s=importlib.util.spec_from_file_location('m',F/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
I=m.interfaces();K=m.kempe(10,I['ten']);print('model ready',flush=True)
M=I['C'].copy();M.update({g:v['F'] for g,v in json.loads((OLD/'C/comparisons.json').read_text())['matrices'].items()})
cat=sorted(map(int,json.loads((OLD/'frozen/artifacts/c5_cells/cells.json').read_text())['cells']))
full=(1<<2461)-1
rows=[0]*2461
for r,i in enumerate(K['rowids']):rows[i]|=1<<r
cols=[(sum(1<<i for i in {K['rowids'][r] for r,v in col}),sum(1<<r for r,v in col)) for col in K['columns']]
def close(live):
 while True:
  covered=0;dead=full^live
  for cb,rb in cols:
   if not cb&dead:covered|=rb
  bad=sum(1<<i for i in range(2461) if live>>i&1 and rows[i]&~covered)
  if not bad:return live
  live^=bad
bits={g:[sum(1<<i for i,v in enumerate(r) if v) for r in mat] for g,mat in M.items()}
zeros={g:{mask:full^sum(1<<i for i in range(2461) if any(mat[j][i] for j in range(10) if not mask>>j&1)) for mask in cat} for g,mat in M.items() if g!='G'}
base=full
for j in (1,4,6):base&=~bits['G'][j]
base=close(base)
def possible(g,mask,live):return all(live&bits[g][r] for r in range(10) if mask>>r&1)
def domains(seed,gs,force={}):
 live=seed;ds={g:force.get(g,cat) for g in gs}
 while True:
  old=live;changed=False
  for g in gs:
   records=[];union=0
   for mask in ds[g]:
    l=close(live&zeros[g][mask])
    if possible('G',941,l) and possible(g,mask,l):records.append(mask);union|=l
   if len(records)!=len(ds[g]):changed=True
   ds[g]=records;live&=union
  if not changed and live==old:break
 print('domains', {g:ds[g] for g in gs},'live',live.bit_count(),flush=True)
 return live,ds
out=[]
for branch,g in [('a1','Q1'),('a2','Q2')]:
 print('BRANCH',branch,flush=True);seed=close(base&~bits[g][9])
 live,ds=domains(seed,['J1','J2','Q1','Q2','GB'],{'J1':[935,942,943]} if branch=='a1' else {'J2':[943]})
 joint=[]
 for j1 in ds['J1']:
  for j2 in ds['J2']:
   l=close(live&zeros['J1'][j1]&zeros['J2'][j2])
   if not possible('G',941,l) or not possible('J1',j1,l) or not possible('J2',j2,l):continue
   ll,d=domains(l,['Q1','Q2','GB'],{k:v for k,v in ds.items() if k not in ('J1','J2')})
   if not ll:continue
   joint.append({'J1':j1,'J2':j2,'domains':d,'live':[i for i in range(2461) if ll>>i&1]})
 print('JOINT',branch,[(r['J1'],r['J2'],r['domains'],len(r['live'])) for r in joint],flush=True)
 out.append({'branch':branch,'joint':joint})
(D/'joint_discovery.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
