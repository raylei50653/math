#!/usr/bin/env python3
"""n=5 diamond subcase: exact direct-edge caps and necessary Kempe closure."""
from pathlib import Path
from itertools import product
import argparse,gzip,hashlib,importlib.util,json
D=Path(__file__).resolve().parent;A=D.parent
F=A/'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen'
P=F/'audits/2026-10-19-r6-941-chains-13dc5ff/A/interface.py'
spec=importlib.util.spec_from_file_location('frozen_interface',P);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
RIM=('a','u2','u1','L','q','c','s','v','w','t')
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
LEFT=(('b','a'),('b','c'),('b','q'),('b','p'),('p','a'),('p','q'),('p','h'),('p','n'),('h','q'),('h','L'),('h','R'),('h','n'),('R','n'),('R','u2'),('R','u1'),('R','L'),('n','a'),('n','u2'))
RIGHT=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','t'),('r','w'),('r','v'),('r','s'))
QL=tuple(e for e in LEFT if not {'p','h'}&set(e))
def canonical(t):
 d={};return tuple(d.setdefault(c,len(d)) for c in t)
def states():
 def grow(t):
  if len(t)==10:
   if t[-1]!=t[0]:yield t
   return
  for c in range(min(3,max(t)+1)+1):
   if c!=t[-1]:yield from grow(t+(c,))
 return list(grow((0,)))
def packed(t):return json.dumps(t,sort_keys=True,separators=(',',':')).encode()
def compute():
 c11path=A/'interface/certificate-v4.json.gz'
 c11=json.load(gzip.open(c11path,'rt'));c11states=[tuple(r['core']) for r in c11['caps']];c11index={t:i for i,t in enumerate(c11states)}
 profile=next(p for p in c11['conditional_chord_profiles'] if p['present_chords']==[['a','u2']])
 c11live=set(profile['live_ids']);assert len(c11live)==3777
 sr=states();assert len(sr)==2461;index={t:i for i,t in enumerate(sr)}
 mats={g:[[0]*len(sr) for _ in ROWS] for g in ('G','Q1','J1')};caps=[];inherit=[]
 for i,t in enumerate(sr):
  base=dict(zip(RIM,t));lifts={}
  for g,vs,es in (('G',('b','p','h','R','n'),LEFT),('Q1',('b','R','n'),QL),('J1',('b','R','n'),QL+(('a','R'),))):
   li=[]
   for v in product(range(4),repeat=len(vs)):
    c=base|dict(zip(vs,v))
    if g=='Q1' and (c['b']!=c['n'] or c['R']!=c['q']):continue
    if g=='J1' and c['b']!=c['L']:continue
    if all(c[u]!=c[v] for u,v in es):li.append(v)
   lifts[g]=li
  right=[]
  for v in product(range(4),repeat=3):
   c=base|dict(zip(('x','y','r'),v))
   if all(c[u]!=c[v] for u,v in RIGHT):right.append(v)
  for g,li in lifts.items():
   for v in li:
    for x,y,r in right:
     row=''.join(map(str,canonical((x,y,base['a'],v[0],base['c']))));mats[g][ROWS.index(row)][i]+=1
  # Exact F' star of n is {a,u2}, so EVERY legal n colour lifts this one F'' colouring.
  alln=[]
  for n in range(4):
   if n in (base['a'],base['u2']):continue
   ext=(base['a'],n,*t[1:]);cid=c11index[canonical(ext)];alln.append((n,cid,cid in c11live))
  if any(not z[2] for z in alln):inherit.append({'core_id':i,'all_n_lifts':alln})
  caps.append({'core':t,'original_left_bphRn':lifts['G'],'Q1_left_bRn':lifts['Q1'],'J1_left_bRn':lifts['J1'],'right_xyr':right,'all_C11_n_lifts':alln})
 capzero={i for i in range(len(sr)) if any(mats['G'][j][i] for j in (1,4,6)) or mats['Q1'][9][i] or any(mats['J1'][j][i] for j in (4,6))}
 zero=capzero|{r['core_id'] for r in inherit};K=old.kempe(10,sr);live,rounds=old.m.close(K,set(range(len(sr)))-zero)
 witnesses=[]
 for e0,e1 in ((0,1),(1,0)):
  literal=(0,2,1,2,3,1,2,e0,e1,2);i=index[canonical(literal)]
  witnesses.append({'literal':literal,'canonical_id':i,'survives':i in live,'J1_left_bRn':caps[i]['J1_left_bRn']})
 return {'status':'necessary n=5 diamond interface; source not realized','ordered_rim':RIM,'interior_named_patch':['p','h','R','n'],'original_n_complete_star':['a','p','h','R','u2'],'Fprime_n_complete_star':['a','u2'],'input_C11_sha256':hashlib.sha256(c11path.read_bytes()).hexdigest(),'states':len(sr),'caps':caps,'matrices_sha256':hashlib.sha256(packed(mats)).hexdigest(),'cap_zero':sorted(capzero),'inherited_C11_zero_lifts':inherit,'initial_zero':sorted(zero),'live':live,'deletion_rounds':rounds,'kempe_columns':len(K['columns']),'witnesses':witnesses,'source_positive_rows_survive':[any(mats['G'][j][i] for i in live) for j in (0,2,3,5,7,8,9)],'source_excluded':False,'smaller_bad_constructed':False,'new_Lean':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--certificate',type=Path,default=D/'diamond-certificate-v2.json.gz');a=p.parse_args();out=json.loads(packed(compute()))
 if a.build:
  with a.certificate.open('xb') as raw:
   with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(packed(out)+b'\n')
 else:assert json.load(gzip.open(a.certificate,'rt'))==out
 print(json.dumps({k:out[k] for k in ('status','states','kempe_columns','witnesses','source_positive_rows_survive','source_excluded')}|{'live_states':len(out['live']),'initial_zero':len(out['initial_zero']),'deletions_by_round':[len(r) for r in out['deletion_rounds']]},sort_keys=True))
if __name__=='__main__':main()
