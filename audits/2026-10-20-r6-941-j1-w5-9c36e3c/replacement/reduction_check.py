#!/usr/bin/env python3
"""Exact full-cap proof certificate for the named n=5 six-rim reduction."""
from pathlib import Path
from itertools import product
import argparse,gzip,json,hashlib
D=Path(__file__).resolve().parent;A=D.parent
SRC=A/'review/diamond-certificate-v2.json.gz'
CAT=A/'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen/audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json'
RIM=('a','u2','u1','L','q','c','s','v','w','t')
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
RIGHT=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','s'),('r','v'),('r','w'),('r','t'))
def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def matrix(caps,drop_equality=None):
 mats=[[0]*len(caps) for _ in ROWS];records=[]
 for i,cap in enumerate(caps):
  t=cap['core'];c=dict(zip(RIM,t));left=[];right=[]
  for b in range(4):
   if b in (c['a'],c['c'],c['q']):continue
   if drop_equality!='a=u1' and c['a']!=c['u1']:continue
   if drop_equality!='b=L' and b!=c['L']:continue
   left.append(b)
  for x,y,r in product(range(4),repeat=3):
   cc=c|{'x':x,'y':y,'r':r}
   if all(cc[u]!=cc[v] for u,v in RIGHT):right.append((x,y,r))
  assert right==[tuple(v) for v in cap['right_xyr']]
  for b in left:
   for x,y,r in right:
    row=''.join(map(str,canonical((x,y,c['a'],b,c['c']))));mats[ROWS.index(row)][i]+=1
  records.append({'core':t,'complete_candidate_b_lifts':left,'complete_original_right_xyr_lifts':right,'ten_coefficients':[m[i] for m in mats]})
 return mats,records

def compute(sourcepath):
 source=json.load(gzip.open(sourcepath,'rt'));caps=source['caps'];live=set(source['live']);assert len(caps)==2461 and len(live)==1889
 assert source['ordered_rim']==list(RIM)
 mats,records=matrix(caps);supports={}
 for j in (1,4,6):
  ids=[i for i,v in enumerate(mats[j]) if v];assert not live.intersection(ids)
  supports[ROWS[j]]=ids
 assert [len(supports[z]) for z in ('01021','01202','01212')]==[24,60,60]
 # Every canonical core outside live has an inherited original-source zero proof.
 assert set(range(2461))-live==set(source['initial_zero'])|{i for rd in source['deletion_rounds'] for i,r in rd}
 positive=[]
 for x,y in ((2,3),(3,2)):
  for v,w in ((2,3),(3,2)):
   # Exact actual d_a extension forced by a1=0 and the original R/n full stars.
   core=(0,2,0,1,2,0,1,v,w,1);i=next(i for i,r in enumerate(records) if tuple(r['core'])==canonical(core))
   c=dict(zip(RIM,core))|{'b':1,'p':3,'h':0,'R':3,'n':1,'x':x,'y':y,'r':0}
   assert c['a']==c['u1'] and c['b']==c['L']
   assert all(c[u]!=c[z] for u,z in RIGHT)
   assert ''.join(map(str,canonical((x,y,0,1,0))))=='01232'
   assert i in live and mats[9][i]>0
   positive.append({'literal_core':core,'literal_xyr':[x,y,0],'canonical_core_id':i})
 catalog=json.loads(CAT.read_text());masks=sorted(set(map(int,catalog['cells'])));assert len(masks)==132
 forbidden=[mask for mask in masks if mask&(1<<9) and not mask&sum(1<<j for j in (1,4,6))]
 assert forbidden==[]
 # Reconstruct full negative caps when either equality is incorrectly omitted:
 # each mutation admits an as-yet-live negative fibre and cannot certify the theorem.
 negative_controls={}
 for equality in ('a=u1','b=L'):
  mm,_=matrix(caps,drop_equality=equality)
  witnesses=[(ROWS[j],i) for j in (1,4,6) for i in live if mm[j][i]]
  assert witnesses
  negative_controls[f'drop {equality}']={'rejected':True,'live_negative_witness':min(witnesses)}
 return {'status':'PASS; actual same-candidate n=5 source reduction','candidate':'(G-{p,h,R,n})/(a=u1,b=L)','original_ordered_frame':['x','y','a','b','c'],'six_rim':['a','b','q','L','u1','u2'],'ordered_core_rim':RIM,'completed_k_delta':-6,'deleted_original_points':['p','h','R','n'],'contracted_disjoint_original_nonedge_arcs':[['a','u1'],['b','L']],'core_states':2461,'source_live_states':1889,'source_sha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'candidate_caps':records,'candidate_matrix_sha256':hashlib.sha256(packed(mats)).hexdigest(),'negative_coefficient_supports':supports,'complete_zero_rows':['01021','01202','01212'],'actual_d_a_literal_positive_lifts':positive,'K132_sha256':hashlib.sha256(CAT.read_bytes()).hexdigest(),'K132_count':132,'K132_masks_accepting_01232_and_rejecting_all_three':forbidden,'negative_controls':negative_controls,'conditional_smaller_bad':True,'n5_source_excluded_by_original_minimality':True,'entire_W5_branch_closed':False,'all_J1_J2_closed':False,'new_Lean':False}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--source',type=Path,default=SRC);ap.add_argument('--certificate',type=Path,default=D/'reduction-certificate.json.gz');a=ap.parse_args();out=json.loads(packed(compute(a.source)))
 if a.build:
  with a.certificate.open('xb') as raw:
   with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(packed(out)+b'\n')
 else:assert json.load(gzip.open(a.certificate,'rt'))==out
 print(json.dumps({k:out[k] for k in ('status','candidate','completed_k_delta','core_states','source_live_states','complete_zero_rows','K132_count','K132_masks_accepting_01232_and_rejecting_all_three','n5_source_excluded_by_original_minimality','entire_W5_branch_closed','all_J1_J2_closed')},sort_keys=True))
if __name__=='__main__':main()
