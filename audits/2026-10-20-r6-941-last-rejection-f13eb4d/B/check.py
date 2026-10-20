#!/usr/bin/env python3
"""Exact c=5/H4-zero compositions and a necessary-model integer control.
Default read-only; --build exclusively creates deterministic gzip certificates.
"""
import argparse,copy,gzip,hashlib,importlib.util,json
from itertools import product
from math import factorial
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'frozen'
BASE='f13eb4d0887d962021992ae7afe3323af4d79cd3'
MODEL='audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
OMODEL='audits/2026-10-19-r6-941-leakage-b89c591/A/model.py'
OLD='audits/2026-10-19-r6-941-chains-13dc5ff/C/check.py'
PREV='audits/2026-10-19-r6-941-existence-f13eb4d/B/check.py'
PREVCERT='audits/2026-10-19-r6-941-existence-f13eb4d/B/certificate.json.gz'
CAT='audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json'
NEEDED=(MODEL,OMODEL,OLD,PREV,PREVCERT,CAT,
 'audits/2026-10-19-r6-941-existence-f13eb4d/SOURCE_CONTRACT.md',
 'audits/2026-10-19-r6-941-existence-f13eb4d/B/PROOF.md',
 'audits/2026-10-19-r6-941-existence-f13eb4d/C/PROOF.md',
 'audits/2026-10-19-r6-941-chains-13dc5ff/PROOF.md',
 'audits/2026-10-19-r6-941-leakage-b89c591/B/SOURCE_CONTRACT.md')
KINDS=('Q1','Q2','J1','J2')

def packed(o):return (json.dumps(o,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(o):return hashlib.sha256(packed(o)).hexdigest()
def load(p,n):
 s=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def authority():
 d=json.loads((HERE.parent/'INPUTS.json').read_text());assert BASE in (HERE.parent/'BASE.md').read_text()
 files={v['path']:v for v in d};out={}
 for p in NEEDED:
  b=(ROOT/p).read_bytes();h=hashlib.sha256(b).hexdigest()
  assert len(b)==files[p]['bytes'] and h==files[p]['sha256'],('frozen drift',p)
  out[p]=h
 return out

def operations(old):
 out=[]
 for hi,(name,frame,edges) in enumerate(old.OPS):
  for j,kind in enumerate(KINDS):
   out.append({'name':name+'_'+kind,'H_index':hi,'left_kind':kind,
    'deleted':['c','p','h'],'boundary':['x','y','a','b',frame],
    'H_added_edges':edges,'left_equalities':((('b','n'),('R','q')), (('b','n'),('b','L')), (('b','L'),), ())[j],
    'left_added_edges':((),(),(('a','R'),),(('a','L'),('a','R'),('b','L')))[j],
    'completed_inner_delta':(-5,-5,-4,-3)[j]})
 return out

def composed(m,old,ten):
 ops=operations(old);Ms=[[[0]*len(ten) for r in m.ROWS] for op in ops];caps=[];fixed_da=[set() for op in ops]
 for i,word in enumerate(ten):
  f=dict(zip(old.PINS,word));rights=[]
  for x,y,r in product(range(4),repeat=3):
   ff=dict(f,x=x,y=y,r=r)
   if all(ff[u]!=ff[v] for u,v in old.RIGHT):rights.append((x,y,r))
  cap=[[] for op in ops]
  for b in range(4):
   if b in (f['a'],f['q']):continue
   for x,y,r in rights:
    ff=dict(f,b=b,x=x,y=y,r=r)
    for j,op in enumerate(ops):
     if not all(ff[u]==ff[v] for u,v in op['left_equalities']):continue
     if not all(ff[u]!=ff[v] for u,v in op['left_added_edges']+op['H_added_edges']):continue
     boundary=tuple(ff[v] for v in op['boundary']);ri=m.ROWS.index(''.join(map(str,m.canonical(boundary))))
     Ms[j][ri][i]+=1;cap[j].append((b,x,y,r))
  fac=factorial(4-len(set(word)))
  for M in Ms:
   for row in M:assert row[i]%fac==0;row[i]//=fac
  caps.append({'core':word,'complete_lifts':cap})
 return ops,Ms,caps

def lift_original_c(m,ten,z):
 ix={t:i for i,t in enumerate(ten)};trans=[];oldz=[]
 for a,n,R,L,q,c,s,v,w,t in ten:
  lifts=[ix[m.canonical((a,n,R,L,q,u,s,v,w,t))] for u in range(4) if u not in {q,c,s}]
  trans.append(lifts);oldz.append(sum(z[i] for i in lifts))
 return trans,oldz

def source_values(m,om,ten,z):
 trans,oldz=lift_original_c(m,ten,z);ix={t:i for i,t in enumerate(ten)};U=[]
 for row in m.ROWS:
  a,s,v,w,t=map(int,row);val=0
  for n,R,L,q in product(range(4),repeat=4):
   core=(a,n,R,L,q,a,s,v,w,t)
   if not m.proper(core):continue
   ph=sum(p not in {a,q,n,h} and h not in {p,q,L,R,n} for p,h in product(range(4),repeat=2))
   val+=ph*oldz[ix[m.canonical(core)]]
  U.append(val)
 pos={name:sum(oldz[i] for i in ids) for name,ids in om.source_positive_subsets(ix).items()}
 return {'original_D10_counts':oldz,'original_c_transfer':trans,'U_counts':U,'U_mask':m.mask(U),'mandatory_sector_counts':pos}

def verify_control(rec,m,om,ten,K,C,Hs,Qs,Ss,Ms,cat,live,parts):
 assert rec['model_only'] is True and rec['source_realized'] is False,'model versus source authority'
 z=rec['core_counts'];assert len(z)==len(ten) and all(type(v) is int and v>=0 for v in z),'nonnegative full core counts'
 assert all(not v for i,v in enumerate(z) if i not in set(live)),'all proved complete zero fibres'
 rebuilt=[0]*len(ten);seen=set()
 for j,v in rec['planar_coefficients']:
  assert type(j) is int and 0<=j<len(parts) and j not in seen and type(v) is int and v,'signed planar coefficient domain';seen.add(j)
  p=parts[j];pairs=[(i,next(k for k in range(i) if p[k]==p[i])) for i in range(10) if p[i] in p[:i]]
  for i,t in enumerate(ten):
   if all(t[a]==t[b] for a,b in pairs):rebuilt[i]+=v
 assert rebuilt==z,'same complete core signed planar span'
 residual=[-K['hsize'][r]*z[i] for r,i in enumerate(K['rowids'])];seen=set()
 for j,v in rec['orbit_weights']:
  assert type(j) is int and 0<=j<len(K['columns']) and j not in seen and type(v) is int and v>0,'positive complete orbit weight';seen.add(j)
  for r,a in K['columns'][j]:residual[r]+=a*v
 assert not any(residual),'complete counted component equations'
 groups={'G':[C],'H':Hs,'Q':Qs,'S':Ss,'composed':Ms};counts={g:[m.mv(M,z) for M in group] for g,group in groups.items()}
 masks={g:[m.mask(v) for v in vs] for g,vs in counts.items()}
 assert masks['G']==[941] and counts['H'][4][0]==0,'full original support and H4 zero'
 assert masks['Q']==[1021,1021],'both original accepting and leaking Qs'
 assert all(s in cat for g,ss in masks.items() if g!='G' for s in ss),'all 28 old and 20 new candidates in catalogue'
 assert masks['H']==[1023,1022,1023,1022,1022],'common five-graph branch26'
 assert masks['composed'][16:20]==[1023]*4,'all four H4 compositions full support'
 source=source_values(m,om,ten,z)
 assert source['U_mask']==319 and all(v>0 for v in source['mandatory_sector_counts'].values()),'U319 and both source-positive sectors'
 return {'counts':counts,'masks':masks,'source':source,'positive_core_fibres':sum(v>0 for v in z),'complete_orbits':len(rec['orbit_weights']),
 'signed_planar_terms':len(rec['planar_coefficients']),'max_absolute_coefficient':max([*z]+[abs(v) for j,v in rec['orbit_weights']+rec['planar_coefficients']]),
 'model_only':True,'source_realized':False,'all_geometric_source_conditions_encoded':False}

def compute():
 inp=authority();m=load(MODEL,'b_model');om=load(OMODEL,'b_oldmodel');old=load(OLD,'b_old');prev=load(PREV,'b_prev')
 ten,C,Hs,Qs,Ss,sops,oldcaps=prev.matrices(m,old)
 oldcert=json.loads(gzip.decompress((ROOT/PREVCERT).read_bytes()))
 assert [C,Hs,Qs,Ss]==[oldcert['original_matrix'],oldcert['H_matrices'],oldcert['Q_matrices'],oldcert['S_matrices']]
 assert digest(oldcaps)==oldcert['complete_caps_sha256'],'all frozen original, Q and S lifts replayed'
 ops,Ms,caps=composed(m,old,ten);K=m.kempe(10,ten);cl=prev.Closure(K,len(ten))
 seed=[i for i in range(len(ten)) if all(not C[r][i] for r in (1,4,6)) and not Hs[4][0][i]]
 live,rounds=cl.close(seed);assert len(live)==1785 and prev.projection(C,live)==941
 assert (live,rounds)==m.close(K,seed),'independent list-set complete zero closure'
 cat=sorted(map(int,json.loads((ROOT/CAT).read_text())['cells']));assert len(cat)==132
 comparisons=[]
 for j,M in enumerate(Ms):
  cases=[]
  for support in cat:
   initial=[i for i in live if all(not M[r][i] for r in range(10) if not support>>r&1)]
   ll,rr=cl.close(initial);original=prev.projection(C,ll);upper=prev.projection(M,ll)
   cases.append({'support':support,'seed':initial,'live':ll,'rounds':rr,'original_upper':original,'candidate_upper':upper,
    'not_excluded_by_zero_closure':original==941 and not(support&~upper)})
  possible=[r['support'] for r in cases if r['not_excluded_by_zero_closure']]
  expected=[1022,1023] if j in (12,13) else [1022] if j in (14,15) else [1023]
  assert possible==expected,(j,possible)
  comparisons.append({'candidate':j,'possible_supports':possible,'comparisons':cases})
 # Every positive composed row is a fibre on its stated new frame.
 normalized_da=[]
 for j in range(16,20):
  ids=[i for i in live if Ms[j][0][i]];words=set()
  for i in ids:
   f=dict(zip(old.PINS,ten[i]))
   for b,x,y,r in caps[i]['complete_lifts'][j]:
    ff=dict(f,b=b,x=x,y=y,r=r);boundary=tuple(ff[v] for v in ops[j]['boundary'])
    if m.canonical(boundary)!=(0,1,0,1,2):continue
    ren={boundary[0]:0,boundary[1]:1,boundary[4]:2};ren[next(c for c in range(4) if c not in ren)]=3
    words.add(tuple(ren[c] for c in ten[i]))
  assert len(ids)==(4,4,6,10)[j-16] and len(words)==len(ids)
  normalized_da.append({'candidate':j,'live_ids':ids,'fixed_H4_01012_core_words':sorted(words)})
 assert all(t[5]==1 for d in normalized_da[2:] for t in d['fixed_H4_01012_core_words']),'J1 and J2 positive H4 d_a forces original u=b'
 parts=[p for p in m.growth(10) if m.proper(p) and m.noncrossing(p)];assert len(parts)==603
 control=json.loads((HERE/'counted-control.json').read_text())
 summary=verify_control(control,m,om,ten,K,C,Hs,Qs,Ss,Ms,cat,live,parts)
 negative=[]
 for name,mutate in (
  ('model cannot become source',lambda r:r.update(source_realized=True)),
  ('all empty fibres retained',lambda r:r['core_counts'].__setitem__(next(i for i in range(len(ten)) if i not in set(live)),1)),
  ('one complete orbit missing',lambda r:r['orbit_weights'].pop()),
  ('signed planar coefficients not discarded',lambda r:r['planar_coefficients'].pop())):
  bad=copy.deepcopy(control);mutate(bad)
  try:verify_control(bad,m,om,ten,K,C,Hs,Qs,Ss,Ms,cat,live,parts)
  except AssertionError:negative.append(name)
  else:raise AssertionError(('negative control accepted',name))
 result={'base':BASE,'inputs':inp,'source_hypothesis':'full frozen r6/941 source plus original c=5 and fixed H4 new-frame 01012 empty',
  'core_order':old.PINS,'core_states':ten,'literal_rows':m.ROWS,'operations':ops,'matrices':Ms,
  'complete_new_caps_sha256':digest(caps),'complete_old_caps_sha256':digest(oldcaps),'component_columns':len(K['columns']),
  'component_columns_sha256':digest(K['columns']),'source_zero_closure':{'seed':seed,'live':live,'rounds':rounds},
  'catalogue':cat,'candidate_comparisons':comparisons,'H4_positive_row0_restrictions':normalized_da,
  'control_sha256':hashlib.sha256((HERE/'counted-control.json').read_bytes()).hexdigest(),'control_summary':summary,
  'negative_controls':negative,'H4_branch_excluded':False,'strict_smaller_bad_constructed':False,'source_realization_supplied':False,
  'no_new_Lean_theorem':True}
 return result,caps

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args();result,caps=compute()
 for name,obj in (('certificate.json.gz',result),('complete-lifts.json.gz',caps)):
  p=HERE/name;data=packed(obj)
  if args.build:
   with p.open('xb') as f:f.write(gzip.compress(data,mtime=0))
  else:assert gzip.decompress(p.read_bytes())==data,('certificate drift',name)
 print(json.dumps({'operations':20,'H4_compositions':[v['possible_supports'] for v in result['candidate_comparisons'][16:]],
  'control':{k:result['control_summary'][k] for k in ('positive_core_fibres','complete_orbits','signed_planar_terms','max_absolute_coefficient')},
  'U_counts':result['control_summary']['source']['U_counts'],'mandatory_sector_counts':result['control_summary']['source']['mandatory_sector_counts'],
  'negative_controls':len(result['negative_controls']),'H4_branch_excluded':False},sort_keys=True))
if __name__=='__main__':main()
