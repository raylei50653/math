#!/usr/bin/env python3
"""Independent literal-edge full-cap audit; no exterior-realizability assertion."""
from pathlib import Path
from itertools import product
from collections import Counter
import argparse,gzip,hashlib,json
D=Path(__file__).resolve().parent
A=D.parent/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c'
IP=A/'interface/certificate-v4.json.gz'
LP=A/'replacement/long-case-certificate.json.gz'
CAT=A/'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen/audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json'
NAMES=('a','n','u2','u1','L','q','c','s','v','w','t')
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
LEFT=(('b','a'),('b','c'),('b','q'),('b','p'),('p','a'),('p','q'),('p','n'),('p','h'),('h','q'),('h','L'),('h','R'),('h','n'),('R','n'),('R','u2'),('R','u1'),('R','L'))
QUOT=(('b','a'),('b','c'),('b','q'),('R','n'),('R','u2'),('R','u1'),('R','L'))
RIGHT=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','s'),('r','v'),('r','w'),('r','t'))
def canon(t):
 d={};return tuple(d.setdefault(v,len(d)) for v in t)
def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def proper(c,edges):return all(c[u]!=c[v] for u,v in edges)
def growth(n,t=(0,)):
 if len(t)==n:
  if t[-1]!=t[0]:yield t
  return
 for c in range(min(3,max(t)+1)+1):
  if c!=t[-1]:yield from growth(n,t+(c,))
def rownum(frame):return ROWS.index(''.join(map(str,canon(frame))))
def compute():
 inter=json.load(gzip.open(IP,'rt'));long=json.load(gzip.open(LP,'rt'))
 states=list(growth(11));assert len(states)==7381
 assert states==[tuple(cap['core']) for cap in inter['caps']]
 live=set(inter['live']);assert len(live)==5951
 mats={name:[[0]*len(states) for _ in ROWS] for name in ('G','Q1','J1','C0','C1')}
 records=[];res={name:{row:Counter() for row in ('01021','01202','01212')} for name in ('C0','C1')}
 mutated_right_changes=[]
 for i,t in enumerate(states):
  c=dict(zip(NAMES,t));left=[];right=[];quot=[];ji=[]
  for values in product(range(4),repeat=4):
   cc=c|dict(zip(('b','p','h','R'),values))
   if proper(cc,LEFT):left.append(values)
  for values in product(range(4),repeat=3):
   cc=c|dict(zip(('x','y','r'),values))
   if proper(cc,RIGHT):right.append(values)
   if proper(cc,tuple(e for e in RIGHT if e!=('r','v'))) and not proper(cc,RIGHT):
    mutated_right_changes.append((i,values))
  for b,R in product(range(4),repeat=2):
   cc=c|{'b':b,'R':R}
   if proper(cc,QUOT) and b==c['n'] and R==c['q']:quot.append((b,R))
   if proper(cc,QUOT+(('a','R'),)) and b==c['L']:ji.append((b,R))
  cap=inter['caps'][i]
  for key,ls in (('original_left_bphR',left),('Q1_left_bR',quot),('J1_left_bR',ji),('right_xyr',right)):
   assert ls==[tuple(v) for v in cap[key]],(i,key)
  for name,ls in (('G',left),('Q1',quot),('J1',ji)):
   for ll in ls:
    for x,y,r in right:mats[name][rownum((x,y,c['a'],ll[0],c['c']))][i]+=1
  candidates={}
  for k,u in enumerate(('u1','u2')):
   name=f'C{k}';bs=[c['L']] if c['a']==c[u] and c['L'] not in (c['a'],c['c'],c['q']) else []
   candidates[name]=bs
   for b in bs:
    for x,y,r in right:
     frame=(x,y,c['a'],b,c['c']);j=rownum(frame);mats[name][j][i]+=1
     if i in live and ROWS[j] in res[name]:
      perm=dict(zip(frame,map(int,ROWS[j])))
      missing=sorted(set(range(4))-set(perm));unused=sorted(set(range(4))-set(perm.values()))
      perm.update(zip(missing,unused));literal=tuple(perm[v] for v in t)
      res[name][ROWS[j]][literal]+=1
  records.append({'core':t,'G_bphR':left,'Q1_bR':quot,'J1_bR':ji,'right_xyr':right,'C0_b':candidates['C0'],'C1_b':candidates['C1'],'ten_coefficients':{name:[m[i] for m in matrix] for name,matrix in mats.items()}})
 original={name:mats[name] for name in ('G','Q1','J1')}
 assert hashlib.sha256(packed(original)).hexdigest()==inter['matrices_sha256']
 cap_zero=sorted(i for i in range(7381) if any(mats['G'][j][i] for j in (1,4,6)) or mats['Q1'][9][i] or any(mats['J1'][j][i] for j in (4,6)))
 assert cap_zero==inter['cap_zero']
 masks=sorted(set(map(int,json.loads(CAT.read_text())['cells'])));assert len(masks)==132
 candidates=[]
 for k in range(2):
  name=f'C{k}';mat=mats[name];old=long['candidates'][k]
  sha=hashlib.sha256(packed(mat)).hexdigest();assert sha==old['matrix_sha256']
  literal={z:[{'literal_core':t,'coefficient':n} for t,n in sorted(cs.items())] for z,cs in res[name].items()}
  assert json.loads(packed(literal))==old['negative_complete_fibres']
  assert all(v['coefficient']==1 for vals in literal.values() for v in vals)
  supports=[[i for i in sorted(live) if mat[j][i]] for j in range(10)]
  mask=sum(1<<j for j,ids in enumerate(supports) if ids)
  assert mask==1023 and mask in masks
  candidates.append({'candidate':name,'matrix_sha256':sha,'maximal_live_complete_support':mask,'maximal_support_in_K132':True,'live_row_support_sizes':dict(zip(ROWS,map(len,supports))),'negative_complete_fibres':literal})
 assert mutated_right_changes
 # These two candidate coefficient supports are disjoint because original u1u2
 # is an edge and therefore no complete core may have a=u1=u2.
 assert not any(any(mats['C0'][j][i] for j in range(10)) and any(mats['C1'][j][i] for j in range(10)) for i in range(7381))
 return {'status':'PASS independent literal-edge cap reconstruction; source OPEN','inputs':{'interface_sha256':digest(IP),'long_case_sha256':digest(LP),'K132_sha256':digest(CAT)},'ordered_rim':NAMES,'original_ordered_frame':['x','y','a','b','c'],'rows':ROWS,'core_states':7381,'inherited_live_upper_bound_size':5951,'caps':records,'cap_zero':cap_zero,'candidate_results':candidates,'negative_controls':{'omit_original_rv_edge':{'changes_full_right_cap':True,'first_extra_lift':mutated_right_changes[0]},'claim_source_exclusion':False},'candidate_K132_support_alone_forces_new_zero':False,'actual_source_realized':False,'source_excluded':False,'new_Lean':False}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'caps-certificate.json.gz');args=ap.parse_args()
 out=json.loads(packed(compute()))
 if args.build:
  with args.certificate.open('xb') as raw:
   with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as dst:dst.write(packed(out)+b'\n')
 else:
  assert json.load(gzip.open(args.certificate,'rt'))==out,'certificate mismatch'
 print(json.dumps({k:out[k] for k in ('status','core_states','inherited_live_upper_bound_size','candidate_K132_support_alone_forces_new_zero','actual_source_realized','source_excluded','new_Lean')}|{'candidates':[{k:v for k,v in c.items() if k!='negative_complete_fibres'} for c in out['candidate_results']]},sort_keys=True))
if __name__=='__main__':main()
