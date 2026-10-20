from pathlib import Path
import importlib.util,json,itertools,time
D=Path(__file__).resolve().parent;J=D.parent/'frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d'
P=J/'frozen/audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
spec=importlib.util.spec_from_file_location('m',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=json.loads((J/'J2/certificate.json').read_text());states=[t for t in m.growth(10,four=True) if m.proper(t)];K=m.kempe(10,states)
live=set(c['live']);rowids=K['rowids'];base_rows=sum(1<<r for r,i in enumerate(rowids) if i in live)
cols=[]
for col in K['columns']:
 ids={rowids[r] for r,v in col}
 if ids<=live:cols.append((sum(1<<i for i in ids),sum(1<<r for r,v in col)))
fs=[f for f in c['forms'] if f['family']!=3 or f['literal_core'][6]==2]
def close(seeds):
 dead=sum(1<<i for i in seeds)
 while 1:
  covered=0
  for ids,rows in cols:
   if not ids&dead:covered|=rows
  holes=base_rows&~covered;new=dead
  while holes:
   bit=holes&-holes;r=bit.bit_length()-1;holes-=bit;new|=1<<rowids[r]
  if new==dead:return {i for i in live if not (dead>>i)&1}
  dead=new
print('reps',[(i,f['family'],f['literal_core']) for i,f in enumerate(fs)],flush=True)
allids={f['core_index'] for f in c['forms']};ans=[]
for n in range(1,11):
 winners=[]
 for ix in itertools.combinations(range(10),n):
  out=close({fs[i]['core_index'] for i in ix})
  if not allids&out:winners.append(ix)
 print(n,'winners',winners,flush=True)
 if winners:
  ans=winners;break
with (D/'j2-minimal-discovery.json').open('x') as f:json.dump({'size':n,'winning_seed_sets':ans,'representatives':fs},f,indent=2)
chosen={f['core_index'] for f in c['forms'] if f['literal_core'][6]==2}
out,rounds=m.close(K,live-chosen)
print('six exact closure',len(out),rounds,flush=True)
for rd in rounds:
 for i,r in rd:
  print('delete',i,'row',r,'hrow',K['hrows'][r],'form',[(f['family'],f['literal_core']) for f in c['forms'] if f['core_index']==i],flush=True)
