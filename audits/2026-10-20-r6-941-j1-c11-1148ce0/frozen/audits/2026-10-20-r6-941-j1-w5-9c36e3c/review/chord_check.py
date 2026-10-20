#!/usr/bin/env python3
"""Independent bitset zero closure over the frozen complete-component family."""
from pathlib import Path
import argparse,gzip,hashlib,importlib.util,json
D=Path(__file__).resolve().parent;A=D.parent
F=A/'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen'
spec=importlib.util.spec_from_file_location('frozen_interface',F/'audits/2026-10-19-r6-941-chains-13dc5ff/A/interface.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def canon(t):
 d={};return tuple(d.setdefault(c,len(d)) for c in t)
def close_bits(K,initial):
 # Independently implement the all-half-palette coverage rule with integer masks.
 rows=K['rowids'];needed=[0]*len(K['states'])
 for h,i in enumerate(rows):needed[i]|=1<<h
 cols=[]
 for c in K['columns']:
  full=half=0
  for h,mul in c:full|=1<<rows[h];half|=1<<h
  cols.append((full,half))
 live=set(initial);rounds=[]
 while True:
  mask=sum(1<<i for i in live);covered=0
  for full,half in cols:
   if not(full&~mask):covered|=half
  rem=sorted(i for i in live if needed[i]&covered!=needed[i])
  if not rem:return sorted(live),rounds
  rounds.append(rem);live.difference_update(rem)
def compute():
 path=A/'interface/certificate-v4.json.gz';source=json.load(gzip.open(path,'rt'));states=[tuple(r['core']) for r in source['caps']]
 K=old.kempe(11,states)
 digest=hashlib.sha256(json.dumps(K['columns'],sort_keys=True,separators=(',',':')).encode()).hexdigest();assert digest==source['kempe']['columns_sha256']
 parent=json.loads((F.parent/'J1/certificate.json').read_text());plive=set(parent['final_live'])
 ten=[t for t in old.m.growth(10,four=True) if old.m.proper(t)];ti={t:i for i,t in enumerate(ten)}
 inherited=set()
 for i,t in enumerate(states):
  a,n,u2,u1,L,q,c,s,v,w,T=t
  for R in range(4):
   if R in (n,u2,u1,L):continue
   if ti[canon((a,n,R,L,q,c,s,v,w,T))] not in plive:inherited.add(i)
 initial=set(source['cap_zero'])|inherited;assert initial==set(source['initial_zero'])
 outcomes=[]
 for chord in (None,('a','u2'),('s','u2'),('v','u2'),('v','u1'),('w','u1')):
  profile=next(p for p in source['conditional_chord_profiles'] if p['present_chords']==([] if chord is None else [list(chord)]))
  eligible=set(range(len(states)))-initial
  if chord:
   u,v=map(source['ordered_rim'].index,chord);eligible={i for i in eligible if states[i][u]!=states[i][v]}
  live,rounds=close_bits(K,eligible)
  assert live==profile['live_ids'];assert rounds==[[z[0] for z in r] for r in profile['deletion_rounds']]
  outcomes.append({'present_chord':chord,'live_states':len(live),'deletions_by_round':list(map(len,rounds)),'matches_parent_exactly':True})
 return {'status':'PASS','method':'independent integer-bitset closure, frozen complete complementary-component columns','source_interface_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kempe_columns_sha256':digest,'columns':len(K['columns']),'initial_zero':len(initial),'profiles':outcomes,'source_pocket_and_component_theorems_reproved':False,'source_excluded':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--certificate',type=Path,default=D/'chord-check.json');a=p.parse_args();out=json.loads(json.dumps(compute()))
 if a.build:
  with a.certificate.open('x') as f:json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
 else:assert json.loads(a.certificate.read_text())==out
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
