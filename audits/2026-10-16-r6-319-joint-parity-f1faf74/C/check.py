#!/usr/bin/env python3
"""Check C custody, every local original five-vertex lift, and necessary screens."""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
P=Path(__file__).resolve().parent
A=P.parent
PATTERNS=('ABABC','ABACB','ABACD','ABCAB','ABCAC','ABCAD','ABCBC','ABCBD','ABCDB','ABCDC')
def canon(rr):
 d={};return tuple(d.setdefault(c,len(d)) for c in rr)
def name(rr):return ''.join('ABCD'[c] for c in rr)
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fibres',type=Path,default=P/'full-source-local-fibres.json');args=ap.parse_args()
 seal=json.loads((P/'certificate.json').read_text())
 for row in seal['inputs']:
  path=A/'frozen'/row['path'];need(digest(path)==row['sha256'],'frozen input hash mismatch: '+row['path'])
 need(digest(P/'cells.json')==seal['catalogue_sha256'],'local catalogue differs from frozen input')
 for row in seal['outputs']:
  need(digest(P/row['path'])==row['sha256'],'worker output hash mismatch: '+row['path'])
 # Independent direct graph check: pins c,s,j,i,w,t,a,p,q,v,r,x,y,b.
 cycle=tuple((i,(i+1)%9) for i in range(9))
 added=((9,1),(9,2),(9,3),(9,4),(9,10),(10,1),(10,5),(10,4),(10,11),(10,12),(11,0),(11,1),(11,12),(12,6),(12,5),(13,6),(13,0),(13,7),(13,8))
 rows=sorted({canon(r) for r in product(range(4),repeat=9) if all(r[i]!=r[j] for i,j in cycle)})
 expected=[]
 for r in rows:
  ll=[]
  for extra in product(range(4),repeat=5):
   whole=r+extra
   if all(whole[i]!=whole[j] for i,j in added):
    frame=canon((whole[11],whole[12],whole[6],whole[13],whole[0]))
    ll.append(list(extra)+( [1<<PATTERNS.index(name(frame))] ))
  expected.append({'row':name(r),'all_lifts':ll})
 fibres=json.loads(args.fibres.read_text())
 need(fibres['fibres']==expected,'full original lift fibre differs, including empty fibres')
 need(fibres['row_count']==len(rows)==820,'proper local row count')
 need(fibres['empty_lift_fibre_count']==sum(not x['all_lifts'] for x in expected)==475,'empty local fibre count')
 need(fibres['total_normalized_local_lifts']==sum(len(x['all_lifts']) for x in expected)==648,'complete local lift count')
 need(fibres['proper_labelled_boundary_count']==24*len(rows)==19680,'global colour orbit count')
 need(fibres['improper_boundary_empty_count']==4**9-24*len(rows)==242464,'improper empty rows')
 for script,out in (('explore_v5.py','v5-exploration.json'),('explore_shared_caps.py','shared-caps-exploration.json'),('explore_full_source.py','full-source-exploration.json'),('explore_combined_source.py','combined-source-exploration.json')):
  proc=subprocess.run([sys.executable,'-B',str(P/script),'--check',str(P/out)],text=True,capture_output=True)
  need(proc.returncode==0,script+' failed: '+proc.stdout+proc.stderr)
 # The ordinary support screen does not carry source-realizability authority.
 shared=json.loads((P/'shared-caps-exploration.json').read_text())
 need(len(shared['survivors'])==1 and shared['survivors'][0]['cap_masks']==[1022,1022],'joint cap support result')
 combined=json.loads((P/'combined-source-exploration.json').read_text())
 need(all(len(x['H_fixed'])==58 and len(x['survivors'])==1 and x['survivors'][0]['caps']==[1022,1022] for x in combined),'full-source common H screen')
 print(json.dumps({'status':'PASS','proper_normalized_F_rows':820,'empty_F_lift_fibres':475,'all_local_F_lifts':648,'H_initial_rows':99,'H_after_hexagon_screen':81,'H_after_original_source_screen':58,'cap_mask_pairs_tested':1521,'only_surviving_cap_masks':[1022,1022],'source_coverage':'not triggered','complete319':'OPEN'},sort_keys=True))
if __name__=='__main__':main()
